import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.api.common.state.{MapStateDescriptor, ValueStateDescriptor}
import org.apache.flink.configuration.Configuration
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.functions.ProcessFunction
import org.apache.flink.streaming.api.functions.sink.{RichSinkFunction, SinkFunction}
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

import java.sql.{Connection, DriverManager, PreparedStatement}
import scala.collection.convert.ImplicitConversions.`iterable AsScalaIterable`

object i {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)

    val kafka_source = KafkaSource.builder()
      .setBootstrapServers("192.168.35.131:9092")
      .setTopics("data_all")
      .setValueOnlyDeserializer(new SimpleStringSchema())
      .setStartingOffsets(OffsetsInitializer.earliest())
      .build()

    val stream1 = env.fromSource(kafka_source, WatermarkStrategy.noWatermarks(), "source1")
      .map(lines => {
        val line = lines.split("~-~-~")
        (line(0), line(4))
      })
      .keyBy(data => true)
      .process( new ProcessFunction[(String, String), (Int, Int)] {
        lazy val title_count = getRuntimeContext.getState(new ValueStateDescriptor[Int]("title_count", classOf[Int]))
        lazy val supplier_map = getRuntimeContext.getMapState(new MapStateDescriptor[String, Int]("supplier_map", classOf[String], classOf[Int]))

        override def processElement(i: (String, String), context: ProcessFunction[(String, String), (Int, Int)]#Context, collector: Collector[(Int, Int)]): Unit = {
          title_count.update(title_count.value() + 1)

          if (i._1.contains("暂无供应商")) {

          } else {
            supplier_map.put(i._2, 1)
          }

          val supplier_count = supplier_map.keys().toList.length
          collector.collect(title_count.value(), supplier_count)
        }
      } )

    stream1.print()

    stream1.addSink(new RichSinkFunction[(Int, Int)] {
      var connection: Connection = _
      var preparedStatement: PreparedStatement = _

      override def open(parameters: Configuration): Unit = {
        val jdbcUrl = "jdbc:mysql://bigdata1:3306/xiecheng_db"
        val username = "root"
        val password = "123456"
        connection = DriverManager.getConnection(jdbcUrl, username, password)
        val sql = "INSERT INTO title_supplier_count (title,supplier) VALUES (?, ?)"
        preparedStatement = connection.prepareStatement(sql)
      }

      override def invoke(value: (Int, Int), context: SinkFunction.Context): Unit = {
        preparedStatement.setInt(1, value._1)
        preparedStatement.setInt(2, value._2)
        preparedStatement.execute()
      }

      override def close(): Unit = {
        if (preparedStatement != null) {
          preparedStatement.close()
        }
        if (connection != null) {
          connection.close()
        }
      }
    })

    env.execute()
  }
}

import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.api.common.state.MapStateDescriptor
import org.apache.flink.configuration.Configuration
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.functions.ProcessFunction
import org.apache.flink.streaming.api.functions.sink.{RichSinkFunction, SinkFunction}
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

import java.sql.{Connection, DriverManager, PreparedStatement}

// 地图>	省份、根据省份划分销售总值> mysql:province_sum:province、sale_sum
object province_sum {
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
        (line(6), line(9))
      })
      .keyBy(data => true)
      .process( new ProcessFunction[(String, String), (String, Int)] {
        lazy val data_map = getRuntimeContext.getMapState(new MapStateDescriptor[String, Int]("data_map", classOf[String], classOf[Int]))
        var data:(Int, String) = _

        override def processElement(i: (String, String), context: ProcessFunction[(String, String), (String, Int)]#Context, collector: Collector[(String, Int)]): Unit = {
          if (i._1.contains("暂无销售")) {
            data = (0, i._2)
          } else {
            val sale = "\\d+".r.findAllIn(i._1).toList.mkString("").toInt
            data = (sale, i._2)
          }

          if (data_map.contains(i._2)) {
            data_map.put(i._2, data_map.get(i._2) + data._1)
          } else {
            data_map.put(i._2, data._1)
          }

          collector.collect(i._2, data_map.get(i._2))
        }
      } )

    stream1.print()

    stream1.addSink(new RichSinkFunction[(String, Int)] {
      var connection: Connection = _
      var preparedStatement: PreparedStatement = _

      override def open(parameters: Configuration): Unit = {
        val jdbcUrl = "jdbc:mysql://bigdata1:3306/xiecheng_db"
        val username = "root"
        val password = "123456"
        connection = DriverManager.getConnection(jdbcUrl, username, password)
        val sql = "REPLACE INTO province_sum (province, sale_sum) VALUES (?, ?)"
        preparedStatement = connection.prepareStatement(sql)
      }

      override def invoke(value: (String, Int), context: SinkFunction.Context): Unit = {
        preparedStatement.setString(1, value._1)
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

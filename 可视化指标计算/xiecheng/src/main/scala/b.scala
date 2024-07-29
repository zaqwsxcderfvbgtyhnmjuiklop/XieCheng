import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.configuration.Configuration
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.functions.ProcessFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

import java.sql.{Connection, DriverManager, PreparedStatement}
import org.apache.flink.streaming.api.functions.sink.{RichSinkFunction, SinkFunction}

// 柱状>	评分、根据评分分组聚合总值> mysql:score_count:score、count
object b {
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
        (line(5), 1)
      })
      .process( new ProcessFunction[(String, Int), (String, Int)] {

        override def processElement(i: (String, Int), context: ProcessFunction[(String, Int), (String, Int)]#Context, collector: Collector[(String, Int)]): Unit = {
          if (i._1.contains("暂无评分")) {

          }else {
            collector.collect(i)
          }
        }
      } )
      .keyBy(_._1)
      .sum(1)

    stream1.print()

    stream1.addSink(new RichSinkFunction[(String, Int)] {
      var connection: Connection = _
      var preparedStatement: PreparedStatement = _

      override def open(parameters: Configuration): Unit = {
        val jdbcUrl = "jdbc:mysql://bigdata1:3306/xiecheng_db"
        val username = "root"
        val password = "123456"
        connection = DriverManager.getConnection(jdbcUrl, username, password)
        val sql = "REPLACE INTO score_count (score, count) VALUES (?, ?)"
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

import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.connector.kafka.sink.{KafkaRecordSerializationSchema, KafkaSink}
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.functions.ProcessFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.util.Collector

// 数据去重
object a {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)

    val kafka_source = KafkaSource.builder()
      .setBootstrapServers("192.168.35.131:9092")
      .setTopics("xiecheng_kafka")
      .setValueOnlyDeserializer(new SimpleStringSchema())
      .setStartingOffsets(OffsetsInitializer.earliest())
      .build()

    val kafka_sink = KafkaSink.builder()
      .setBootstrapServers("bigdata1:9092")
      .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setValueSerializationSchema(new SimpleStringSchema())
        .setTopic("data_all")
        .build()
      ).build()

    val stream1 = env.fromSource(kafka_source, WatermarkStrategy.noWatermarks(), "source1")
      .map(line => (line,1))
      .keyBy(_._1)
      .sum(1)
      .process(new ProcessFunction[(String, Int), String] {
        override def processElement(i: (String, Int), context: ProcessFunction[(String, Int), String]#Context, collector: Collector[String]): Unit = {
          if (i._2 == 1){
            collector.collect(i._1)
          }
        }
      })

    stream1.print()

    stream1.sinkTo(kafka_sink)

    env.execute()
  }
}

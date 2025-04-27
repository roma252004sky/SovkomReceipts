package ru.vinpin.SovkomMain.config;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.RoundRobinPartitioner;
import org.apache.kafka.common.serialization.ByteArrayDeserializer;
import org.apache.kafka.common.serialization.ByteArraySerializer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.kafka.receiver.ReceiverOptions;
import reactor.kafka.sender.SenderOptions;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaConfig {
    @Value("${sovkom.kafka.servers}")
    private String servers;
    @Bean
    public SenderOptions<String, byte[]> senderOptions() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, servers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, ByteArraySerializer.class);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, RoundRobinPartitioner.class);
        props.put(ProducerConfig.MAX_REQUEST_SIZE_CONFIG, 300 * 1024 * 1024);
        props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 1024 * 1024 * 1024);
        return SenderOptions.create(props);
    }

    @Bean
    public ReceiverOptions<String, byte[]> receiverOptions() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, servers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "groupSovkomMain");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, ByteArrayDeserializer.class);
        return ReceiverOptions.create(props);
    }

    @Bean
    public ReactiveKafkaProducerTemplate<String, byte[]> reactiveKafkaProducerTemplate(SenderOptions<String, byte[]> senderOptions) {
        return new ReactiveKafkaProducerTemplate<>(senderOptions);
    }


    @Bean
    public WebClient clickHouseWebClient() {
        return WebClient.builder()
                .baseUrl("http://clickhouse-server:8123")
                .defaultHeaders(headers -> headers.setBasicAuth("admin", "admin"))
                .build();
    }

    @Bean
    public ReactiveKafkaConsumerTemplate<String, byte[]> reactiveKafkaConsumerTemplate(ReceiverOptions<String, byte[]> receiverOptions){
        return new ReactiveKafkaConsumerTemplate<>(receiverOptions);
    }
}

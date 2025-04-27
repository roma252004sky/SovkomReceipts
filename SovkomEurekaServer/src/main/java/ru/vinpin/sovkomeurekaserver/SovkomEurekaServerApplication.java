package ru.vinpin.sovkomeurekaserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@EnableEurekaServer
@SpringBootApplication
public class SovkomEurekaServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(SovkomEurekaServerApplication.class, args);
    }

}

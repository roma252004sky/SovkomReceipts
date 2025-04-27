FROM gradle:8.7-jdk17 AS build

WORKDIR /app

COPY build.gradle .
COPY settings.gradle .
RUN gradle dependencies --no-daemon
COPY src ./src
RUN gradle bootJar --no-daemon --build-cache

FROM openjdk:17-jdk-slim

RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app
COPY --from=build /app/build/libs/SovkomEurekaServer.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
EXPOSE 80
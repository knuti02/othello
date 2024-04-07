# Use the official Maven image with a tag specifying the JDK version
FROM maven:3.8.4-openjdk-17

# Set the working directory in the container
WORKDIR /app

# Copy the Java application's source code into the container
COPY src ./src
COPY pom.xml .

# Build the application
RUN mvn clean package

# Specify the entry point to run the jar
ENTRYPOINT ["java", "-jar", "target/othello-backend-1.0-SNAPSHOT.jar"]
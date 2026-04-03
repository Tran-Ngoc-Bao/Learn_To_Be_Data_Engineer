# ☕ Java — Learning Guide (for Data Engineers)

> Java is a strongly typed, object-oriented language widely used across the Big Data ecosystem (Hadoop, Hive, HBase, Kafka clients, Flink, and Spark internals).  
> Goal: learn **enough Java to be effective as a Data Engineer** (read code, write small utilities/jobs, debug, build, and deploy).

---

## 🗺️ Suggested Roadmap

1. Java basics: syntax, types, control flow
2. OOP: classes, interfaces, inheritance, polymorphism
3. Collections + Generics
4. Exceptions + Logging
5. File I/O + JSON + HTTP
6. Concurrency basics
7. Build tools: Maven / Gradle
8. Testing: JUnit
9. Packaging & best practices

---

## 1. Environment Setup

### Install
- JDK: **Temurin/OpenJDK 17** (recommended LTS)
- IDE: IntelliJ IDEA or VS Code (+ Extension Pack for Java)

### Verify
```bash
java -version
javac -version
```

---

## 2. Java Basics

### Hello World
```java
public class Main {
  public static void main(String[] args) {
    System.out.println("Hello Java");
  }
}
```

### Primitive Types
| Type | Example |
|---|---|
| `int` | `int a = 10;` |
| `long` | `long x = 10L;` |
| `double` | `double p = 3.14;` |
| `boolean` | `boolean ok = true;` |
| `char` | `char c = 'A';` |

> `String` is an object: `String s = "abc";`

### Control Flow
```java
if (x > 0) { ... } else { ... }

for (int i = 0; i < 3; i++) { ... }

while (cond) { ... }

switch (status) {
  case "OK" -> System.out.println("ok");
  default -> System.out.println("other");
}
```

---

## 3. OOP (Essential for Reading Big Data Code)

### Class + Constructor
```java
public class User {
  private final String name;
  private int age;

  public User(String name, int age) {
    this.name = name;
    this.age = age;
  }

  public String getName() { return name; }
  public int getAge() { return age; }
  public void setAge(int age) { this.age = age; }
}
```

### Inheritance + Polymorphism
```java
class Animal { void sound() { System.out.println("..."); } }
class Dog extends Animal { @Override void sound() { System.out.println("woof"); } }

Animal a = new Dog();
a.sound(); // woof
```

### Interface
```java
interface Storage {
  void put(String key, String value);
}

class InMemoryStorage implements Storage {
  public void put(String key, String value) { ... }
}
```

---

## 4. Collections & Generics

### List / Map / Set
```java
import java.util.*;

List<String> names = new ArrayList<>();
names.add("Bao");

Map<String, Integer> scores = new HashMap<>();
scores.put("A", 10);

Set<String> uniq = new HashSet<>();
uniq.add("x");
```

### Generics
```java
public static <T> List<T> singleton(T value) {
  return List.of(value);
}
```

---

## 5. Exceptions

```java
try {
  int x = Integer.parseInt("12");
} catch (NumberFormatException e) {
  // handle
} finally {
  // always runs
}
```

### Checked vs Unchecked
- **Checked**: must be caught/declared (e.g., `IOException`)
- **Unchecked**: runtime exceptions (e.g., `NullPointerException`)

---

## 6. File I/O (Common in ETL Utilities)

```java
import java.nio.file.*;

String content = Files.readString(Path.of("input.txt"));
Files.writeString(Path.of("out.txt"), content.toUpperCase());
```

---

## 7. HTTP + JSON (Real-world DE Work)

### HTTP (Java 11+)
```java
import java.net.URI;
import java.net.http.*;

HttpClient client = HttpClient.newHttpClient();
HttpRequest req = HttpRequest.newBuilder()
  .uri(URI.create("https://httpbin.org/get"))
  .GET()
  .build();

HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
System.out.println(res.body());
```

### JSON Libraries
- Jackson (`com.fasterxml.jackson`)
- Gson

> In production code, you typically parse JSON into POJOs (plain Java objects).

---

## 8. Concurrency Basics

### Thread pool
```java
import java.util.concurrent.*;

ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> 1 + 2);
System.out.println(f.get());
pool.shutdown();
```

---

## 9. Build & Dependencies (Maven)

```bash
mvn -q -DskipTests package
```

Key concepts:
- `pom.xml` defines dependencies, plugins, build config
- Output is usually a `.jar` used by your job/runtime

---

## 10. Testing (JUnit)

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathTest {
  @Test
  void testAdd() {
    assertEquals(3, 1 + 2);
  }
}
```

---

## 11. What Java Skills Matter Most for Data Engineers?

### Must-have
- OOP + interfaces
- Collections + generics
- Exceptions + logging
- Maven/Gradle
- File I/O, JSON
- CLI args and environment variables

### Nice-to-have
- JVM memory basics (heap, GC) for OOM debugging
- Concurrency patterns

---

## 📎 References
- Java Tutorials: https://docs.oracle.com/javase/tutorial/
- Java 17 API: https://docs.oracle.com/en/java/javase/17/docs/api/
- Maven Guides: https://maven.apache.org/guides/
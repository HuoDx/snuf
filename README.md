Simple Networking UDP Framework (SNUF)
===

a.k.a. Stupid Networking UDP Framework  *LOL*

by queuehuo@keeer.net

This is a server framework that feels like Flask, but with UDP protocol and uses JSON for serializing data (that's why I call it stupid lol).

## Goals

  - Easy to use: This project is created for a P2P chat demo for my high school's computer science class, so it should be easy enough for coding beginners to use.
  - Easy to understand: Due to similar reasons, I want this framework to be as simple and intuitive as possible. Hence, performance and optimizations are not the **primary** goal of this project.
  - Works: This framework should be working.

## Design

SNUF uses a separate process to listen, and separate threads to parse and respond to messages. After a message is recieved, the raw (unparsed) message is pushed to a parsing queue maintained by the message parsing thread. When messages are parsed, they will be pushed to another thread that calls a user-defined callback function for message processing. Operations such as "responding" to a message is NOT included in this framework, but will be available by a utility tool provided in this framework to save your time.

### Multi-threading & Multi-processing

As SNUF does not use Python's `asyncio` module, the asynchronous mechanism is fully implemented using a plain event queue (simple, but it works and demands way less learning). Every thread has an event queue to maintain, containing the event data the thread needs to process. 

When the server wants to shut down, a special event, noted as a ThreadStopSignal object is pushed to the queue, and the loop stops when it detects this object. Theoretically, when the object is pushed to the event queue that a thread it maintaining, the `join()` method can be called as the thread will exit soon.

The messages in a thread is not limited to a specific type, but it can never be a ThreadStopSignal unless it is used for stopping the thread. In SNUF,  the data parsing thread takes bytes objects, while the message processing thread takes JSON objects.


###  Message Serialization/Deserialization

A figure worth a thousand words.

The serialization is like:

```
       +----------------+
       | Message Object |
       +----------------+
                |
                V
         +-------------+
         | JSON Object |
         +-------------+   
                |
                V
 +------------------------------+
 | JSON String (UTF-8 encoding) |
 +------------------------------+  
                |
                V
    +------------------------+
    | Bytes (UTF-8 encoding) |
    +------------------------+
```

Similarly, deserialization is like:

```
       +----------------+
       | Message Object |
       +----------------+
                ^
                |
         +-------------+
         | JSON Object |
         +-------------+   
                ^
                |
 +------------------------------+
 | JSON String (UTF-8 encoding) |
 +------------------------------+  
                ^
                |
    +------------------------+
    | Bytes (UTF-8 encoding) |
    +------------------------+
    
```

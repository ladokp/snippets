package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

// WebSocket upgrader to handle incoming connections
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

// Chatroom manages connected clients and message broadcasting
type Chatroom struct {
	clients   map[*websocket.Conn]bool
	broadcast chan string
	mutex     sync.Mutex
}

// NewChatroom creates a new chatroom instance
func NewChatroom() *Chatroom {
	return &Chatroom{
		clients:   make(map[*websocket.Conn]bool),
		broadcast: make(chan string),
	}
}

// Run starts the message broadcasting loop
func (c *Chatroom) Run() {
	for {
		msg := <-c.broadcast
		c.mutex.Lock()
		for client := range c.clients {
			err := client.WriteMessage(websocket.TextMessage, []byte(msg))
			if err != nil {
				client.Close()
				delete(c.clients, client)
			}
		}
		c.mutex.Unlock()
	}
}

// HandleConnection processes WebSocket connections
func (c *Chatroom) HandleConnection(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade failed:", err)
		return
	}
	defer conn.Close()

	c.mutex.Lock()
	c.clients[conn] = true
	c.mutex.Unlock()

	// Read messages and broadcast them
	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			c.mutex.Lock()
			delete(c.clients, conn)
			c.mutex.Unlock()
			break
		}
		c.broadcast <- fmt.Sprintf("User: %s", msg)
	}
}

// Start the web server
func main() {
	chatroom := NewChatroom()
	go chatroom.Run()

	http.HandleFunc("/ws", chatroom.HandleConnection)

	fmt.Println("📡 Chat server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

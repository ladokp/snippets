package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
)

// Secret key for signing JWT tokens
var jwtSecret = []byte("supersecretkey")

// WebSocket Upgrader
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

// Chatroom struct to manage connected clients
type Chatroom struct {
	clients   map[*websocket.Conn]string // Stores client connections and usernames
	broadcast chan string
	mutex     sync.Mutex
}

// NewChatroom creates a new chatroom
func NewChatroom() *Chatroom {
	return &Chatroom{
		clients:   make(map[*websocket.Conn]string),
		broadcast: make(chan string),
	}
}

// Run listens for messages and broadcasts them
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

// Authenticate and extract username from JWT token
func authenticate(r *http.Request) (string, error) {
	tokenString := r.URL.Query().Get("token")
	if tokenString == "" {
		return "", fmt.Errorf("missing token")
	}

	claims := jwt.MapClaims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return jwtSecret, nil
	})

	if err != nil || !token.Valid {
		return "", fmt.Errorf("invalid token")
	}

	username, ok := claims["username"].(string)
	if !ok {
		return "", fmt.Errorf("invalid username in token")
	}

	return username, nil
}

// Handle WebSocket connections with authentication
func (c *Chatroom) HandleConnection(w http.ResponseWriter, r *http.Request) {
	username, err := authenticate(r)
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade failed:", err)
		return
	}
	defer conn.Close()

	c.mutex.Lock()
	c.clients[conn] = username
	c.mutex.Unlock()

	c.broadcast <- fmt.Sprintf("🔵 %s joined the chat", username)

	// Read messages and broadcast them
	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			c.mutex.Lock()
			delete(c.clients, conn)
			c.mutex.Unlock()
			c.broadcast <- fmt.Sprintf("❌ %s left the chat", username)
			break
		}
		c.broadcast <- fmt.Sprintf("💬 %s: %s", username, msg)
	}
}

// Generate JWT token for a given username
func generateToken(username string) (string, error) {
	claims := jwt.MapClaims{
		"username": username,
		"exp":      time.Now().Add(time.Hour * 1).Unix(), // Token expires in 1 hour
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}

// HTTP handler to get a token
func tokenHandler(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Query().Get("username")
	if username == "" {
		http.Error(w, "Username is required", http.StatusBadRequest)
		return
	}

	token, err := generateToken(username)
	if err != nil {
		http.Error(w, "Failed to generate token", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte(token))
}

// Start the chat server
func main() {
	chatroom := NewChatroom()
	go chatroom.Run()

	http.HandleFunc("/ws", chatroom.HandleConnection)
	http.HandleFunc("/token", tokenHandler)

	fmt.Println("📡 Secure Chat Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

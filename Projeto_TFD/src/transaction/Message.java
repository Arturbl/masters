package transaction;



// Enum for Message type
enum MessageType {
    PROPOSE,
    VOTE,
    ECHO
}
class Message {
    private MessageType type;
    private Object content;
    private int sender;

    public Message(MessageType type, Object content, int sender) {
        this.type = type;
        this.content = content;
        this.sender = sender;
    }

    // Getters and setters for all fields
    public MessageType getType() {
        return type;
    }

    public void setType(MessageType type) {
        this.type = type;
    }

    public Object getContent() {
        return content;
    }

    public void setContent(Object content) {
        this.content = content;
    }

    public int getSender() {
        return sender;
    }

    public void setSender(int sender) {
        this.sender = sender;
    }

    // Other methods, if needed
    // For example, a method to display message details
    public void displayMessage() {
        System.out.println("Message Type: " + type);
        System.out.println("Sender: " + sender);
        System.out.println("Content: " + content.toString());
    }
}
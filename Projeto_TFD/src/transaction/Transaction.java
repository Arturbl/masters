/*
*Sender (integer): the sender of the transaction.
• Receiver (integer): the receiver of the transaction.
• Transaction id (integer): a nonce that together with the sender should form a unique id for the tx.
• Amount (double): the amount to be transferred
 */
package transaction;
import java.util.Random;

public class Transaction {
    private double amountSender;
    private double amountReceiver;

    public static String sender;
    public static String receiver;
    public int transactionID;
    public static double amount;


    public Transaction(String sender, String receiver, double amount) {
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
        this.amountSender = generateRandomAmount();
        this.amountReceiver = generateRandomAmount();
    }

    public Transaction() {    //SEM IDEIAS
        return ;
    }
    

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }

    public String getReceiver() {
        return receiver;
    }

    public void setReceiver(String receiver) {
        this.receiver = receiver;
    }

    
    public void setTransactionId(int transactionId) {
        this.transactionID = transactionId;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }
    
    
    private double generateRandomAmount() {
        Random random = new Random();
        return random.nextInt(10000);
    }

    public void showInitialBalance() {
        System.out.println("Sender: " + sender);
        System.out.println("Receiver: " + receiver);
        System.out.println("Initial Sender's Amount: " + amountSender);
        System.out.println("Initial Receiver's Amount: " + amountReceiver);
    }

    public void performTransaction() {
        amountSender -= amount;
        amountReceiver += amount;
        showUpdatedBalance();
    }

    public void showUpdatedBalance() {
        System.out.println("Sender's Updated Amount: " + amountSender);
        System.out.println("Receiver's Updated Amount: " + amountReceiver);
    }
    
    public static void main(String[] args) {
        Transaction transaction = new Transaction("Pedro", "joao", 10);
        transaction.showInitialBalance();

        System.out.println("Sender: " + transaction.getSender());
        System.out.println("Receiver: " + transaction.getReceiver());
        System.out.println("Amount: " + transaction.getAmount());

        transaction.performTransaction();
    }
}




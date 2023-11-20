package transaction;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

public class Block {

    private int blockId;
    private int previousBlockId;
    private byte[] hash;
    private Transaction[] transactions;
    private int length;
    private long timestamp;

    public Block(int blockId, int previousBlockId, byte[] hash, Transaction[] transactions, int length, long timestamp) {
        this.blockId = blockId;
        this.previousBlockId = previousBlockId;
        this.hash = hash;
        this.transactions = transactions;
        this.length = length;
        this.timestamp = timestamp;
    }

    public int getBlockId() {
        return blockId;
    }

    public int getPreviousBlockId() {
        return previousBlockId;
    }

    public byte[] getHash() {
        return hash;
    }

    public Transaction[] getTransactions() {
        return transactions;
    }

    public int getLength() {
        return length;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void calculateHash() {
        String transactionDetails = new String(hash) + blockId + previousBlockId + length + timestamp;
        String newBlockHash = Hash.SHA1(transactionDetails);
        hash = newBlockHash.getBytes();
    }

    public static Block initializeGenesisBlock() {
        // Supondo que o primeiro bloco tenha um hash inicial vazio
        byte[] initialHash = new byte[0];
        Transaction[] transactions = new Transaction[0];
        return new Block(0, -1, initialHash, transactions, 0, System.currentTimeMillis());
    }

    private static class Hash {
        public static String SHA1(String input) {
            try {
                MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
                sha1.update(input.getBytes());
                byte[] digest = sha1.digest();

                StringBuilder hexString = new StringBuilder();
                for (byte b : digest) {
                    hexString.append(String.format("%02x", b));
                }

                return hexString.toString();
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
                return null;
            }
        }
    }

    public void simulateEpochs(int roundsPerEpoch, long epochDurationInMillis) {
        long startTime = System.currentTimeMillis();

        for (int epoch = 1; ; epoch++) {
            System.out.println("Epoch: " + epoch);

            for (int round = 1; round <= roundsPerEpoch; round++) {
                System.out.println("Round: " + round);

                proposeNewBlock(); // Or perform other actions for each round
                calculateHash();
                 // Calculate hash for the new block
            }

            long currentTime = System.currentTimeMillis();
            long elapsedTime = currentTime - startTime;

            if (elapsedTime >= epochDurationInMillis) {
                break;
            }

            // Wait for the remaining epoch duration
            try {
                long remainingTime = epochDurationInMillis - elapsedTime;
                Thread.sleep(remainingTime);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }


    private static class Transactions {
        public Transaction[] getTransactions() {
            Random random = new Random();
            int numberOfTransactions = random.nextInt(10) + 1; // 1 to 10
            Transaction[] transactions = new Transaction[numberOfTransactions];
            for (int i = 0; i < numberOfTransactions; i++) {
                transactions[i] = new Transaction();
            }
            return transactions;
        }
    }

    private List<Block> notarizedChain;
    private int designatedLeader;

    public Block() {
        this.notarizedChain = new ArrayList<>();
        this.designatedLeader = selectDesignatedLeader();
    }

    public int getDesignatedLeader() {
        return designatedLeader;
    }

    public void proposeNewBlock() {
        Block previousBlock = (notarizedChain.isEmpty()) ? null : notarizedChain.get(notarizedChain.size() - 1);
        byte[] previousBlockHash = (previousBlock != null) ? previousBlock.getHash() : new byte[0];

        String transactionDetails = new String(previousBlockHash) + System.currentTimeMillis() + designatedLeader;
        String newBlockHash = Hash.SHA1(transactionDetails);

        Transactions transactions = new Transactions(); // Create new transactions object
        Block newBlock = new Block(
                notarizedChain.size(),
                (previousBlock != null) ? previousBlock.getBlockId() : -1,
                newBlockHash.getBytes(),
                transactions.getTransactions(),
                notarizedChain.size() + 1, // Length of the block in the blockchain
                new Date().getTime()
        );

        notarizedChain.add(newBlock);
        newBlock.calculateHash();

        System.out.println("Block proposed by leader " + designatedLeader + ": " + newBlock.getBlockId());
        System.out.println("Block Hash: " + newBlockHash);
        System.out.println("Block Length: " + newBlock.getLength());
        System.out.println("Block Timestamp: " + newBlock.getTimestamp());
    }

    private int selectDesignatedLeader() {
        Random random = new Random();
        return random.nextInt(8); // 0 to 7
    }

    public static void main(String[] args) {
        Block block = new Block();
        Block genesisBlock = initializeGenesisBlock();
        int designatedLeader = genesisBlock.getDesignatedLeader();
        //int designatedLeader = block.getDesignatedLeader();

        System.out.println("Designated Leader for this Block: " + designatedLeader);
        block.simulateEpochs(24, 24 * 60 * 60 * 1000); // 24 rounds per epoch and 24 hours epoch duration


        Transaction transaction = new Transaction("Pedro", "Joao", 50);
        transaction.showInitialBalance();


        // Realizar a transação e mostrar os valores atualizados
        transaction.performTransaction();
        block.proposeNewBlock();
        block.proposeNewBlock();
    }
}
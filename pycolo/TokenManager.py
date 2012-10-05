# -*- coding:utf-8 -*-


class TokenManager:
    """
    The TokenManager stores all tokens currently used in transfers. New
    transfers can acquire unique tokens from the manager.
    """
    # the empty token, used as default value
    emptyToken = 0
    
    private static TokenManager singleton = new TokenManager()

// Members ///////////////////////////////////////////////////////////////////// 
    
    private Set < byte[] > acquiredTokens = new HashSet < byte[] > ();

    private long currentToken;
    
// Constructors //////////////////////////////////////////////////////////////// 
    
    /** 
     * Default singleton constructor.
     * / 
    private TokenManager() {
        this.currentToken = (long) (Math.random() * 0x100l);
    }
    /* 
    public static TokenManager getInstance() {
        if (singleton == null) {
            synchronized (Communicator.class) {
                if (singleton == null) {
                    singleton = new TokenManager();
                }
            }
        }
        return singleton;
    }
    * / 
    /** 
     * Returns the next message ID to use out of the consecutive 16 - bit range.
     * 
     * @return the current message ID
     */ 
    /* 
    private byte[] nextToken() {

        + +this.currentToken;
        
        logging.info("Token value: ", currentToken);

        long temp = this.currentToken;
        ByteArrayOutputStream byteStream = new ByteArrayOutputStream(OptionNumberRegistry.TOKEN_LEN);  

        while (temp > 0 && byteStream.size() < OptionNumberRegistry.TOKEN_LEN) {
            byteStream.write((int)(temp & 0xff));
            temp >>>= 8;
        }
        
        return byteStream.toByteArray();
    }
    * / 
    
    /* 
     * Returns an unique token.
     * 
     * @param preferEmptyToken If set to true, the caller will receive
     * the empty token if it is available. This is useful for reducing
     * datagram sizes in transactions that are expected to complete
     * in short time. On the other hand, empty tokens are not preferred
     * in block - wise transfers, as the empty token is then not available
     * for concurrent transactions.
     * 
     * / 
    /* 
    public synchronized byte[] acquireToken(boolean preferEmptyToken) {
        
        byte[] token = null;
        if (preferEmptyToken && acquiredTokens.add(emptyToken)) {
            token = emptyToken;
        } else {
            do {
                token = nextToken();
            } while (! acquiredTokens.add(token));
        }
        
        return token;
    }
    * / 
    
    public byte[] acquireToken() {
        return acquireToken(false);
    }
    
    /* 
     * Releases an acquired token and makes it available for reuse.
     * 
     * @param token The token to release
     */ 
    /* 
    public synchronized void releaseToken(byte[] token) {
        
        if (! acquiredTokens.remove(token)) {
            logging.warning(String.format("Token to release is not acquired: %s\n", Option.hex(token)));
        }
    }
    * / 
    
    /* 
     * Checks if a token is acquired by this manager.
     * 
     * @param token The token to check
     * @return True iff the token is currently in use
     */ 
    /* 
    public synchronized boolean isAcquired(byte[] token) {
        return acquiredTokens.contains(token);
    }
    * / 
    
}
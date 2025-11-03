"""Script to initialize the knowledge base with sample support data."""

from rag_search import RAGSearcher


def initialize_sample_knowledge():
    """Initialize knowledge base with sample customer support information."""
    
    rag = RAGSearcher()
    
    # Sample customer support documents
    documents = [
        # Product Information
        "Our product is available in three tiers: Basic ($9.99/month), Pro ($29.99/month), and Enterprise (custom pricing). All plans include 24/7 customer support.",
        
        "The Basic plan includes up to 5 users, 10GB storage, and basic features. The Pro plan includes up to 50 users, 100GB storage, and advanced features. Enterprise plan offers unlimited users and storage.",
        
        # Account Management
        "To reset your password, go to the login page and click 'Forgot Password'. You'll receive an email with instructions to reset your password within 5 minutes.",
        
        "You can upgrade or downgrade your plan at any time from your account settings. Changes take effect immediately, and we'll prorate any charges or credits.",
        
        "To cancel your subscription, go to Account Settings > Billing > Cancel Subscription. You'll retain access until the end of your current billing period.",
        
        # Technical Support
        "If you're experiencing login issues, first clear your browser cache and cookies. If the problem persists, try using an incognito/private window or a different browser.",
        
        "Our service is compatible with all modern web browsers including Chrome, Firefox, Safari, and Edge. We recommend keeping your browser up to date for the best experience.",
        
        "For API integration, you'll need to generate an API key from your account dashboard. Our API documentation is available at docs.example.com/api.",
        
        # Billing
        "We accept all major credit cards (Visa, Mastercard, American Express, Discover) and PayPal. Payment is processed securely through Stripe.",
        
        "Invoices are sent automatically via email at the beginning of each billing cycle. You can also download past invoices from your account settings.",
        
        "We offer a 30-day money-back guarantee for all new subscriptions. If you're not satisfied, contact support within 30 days for a full refund.",
        
        # Features
        "You can export your data at any time in CSV or JSON format from the Data Management section of your dashboard.",
        
        "We perform automated backups daily. Your data is stored redundantly across multiple data centers for maximum reliability.",
        
        "Two-factor authentication (2FA) is available for all accounts. We highly recommend enabling it for additional security. You can set it up in your security settings.",
        
        # Contact Information
        "Our customer support team is available 24/7 via email at support@example.com, phone at 1-800-SUPPORT, or live chat on our website.",
        
        "For sales inquiries, please contact our sales team at sales@example.com or call 1-800-SALES-00 during business hours (9 AM - 6 PM EST).",
    ]
    
    # Metadata for each document
    metadatas = [
        {"category": "pricing", "topic": "plans"},
        {"category": "pricing", "topic": "plan_features"},
        {"category": "account", "topic": "password_reset"},
        {"category": "account", "topic": "plan_changes"},
        {"category": "account", "topic": "cancellation"},
        {"category": "technical", "topic": "login_issues"},
        {"category": "technical", "topic": "browser_compatibility"},
        {"category": "technical", "topic": "api"},
        {"category": "billing", "topic": "payment_methods"},
        {"category": "billing", "topic": "invoices"},
        {"category": "billing", "topic": "refunds"},
        {"category": "features", "topic": "data_export"},
        {"category": "features", "topic": "backups"},
        {"category": "features", "topic": "security"},
        {"category": "contact", "topic": "support"},
        {"category": "contact", "topic": "sales"},
    ]
    
    # Add documents to knowledge base
    print("Initializing knowledge base with sample data...")
    rag.add_documents(documents, metadatas)
    
    # Verify
    count = rag.get_document_count()
    print(f"Knowledge base initialized with {count} documents")
    
    # Test search
    print("\nTesting RAG search...")
    test_query = "How do I reset my password?"
    results = rag._rag_search(test_query, top_k=3)
    
    print(f"\nQuery: {test_query}")
    print(f"Found {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['document'][:100]}...")
        print(f"   Category: {result['metadata'].get('category', 'N/A')}")
        print(f"   Distance: {result['distance']:.4f}\n")


if __name__ == "__main__":
    initialize_sample_knowledge()

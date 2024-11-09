from swarm import Agent

def initialize_enhanced_agents(system):
    """Initialize all agents with their specific roles and functions"""
    
    agents = {}
    
    # Sales Agent
    agents["sales"] = Agent(
        name="Sales Agent",
        instructions="""You are an enthusiastic sales representative with deep product knowledge.
        - Keep responses under 50 words
        - If technical questions arise, transfer to Technical Agent
        - If implementation questions arise, transfer to Customer Success
        - For pricing structure questions, consider transferring to Billing
        - Share specific case studies when relevant
        Base pricing: $30/user/month (standard), $50/user/month (premium).""",
        functions=[
            system.transfer_to_technical,
            system.transfer_to_billing,
            system.transfer_to_success,
            system.transfer_to_support,
            system.check_customer_fit
        ]
    )
    
    # Technical Agent
    agents["technical"] = Agent(
        name="Technical Agent",
        instructions="""You are a technical expert with deep system knowledge.
        - Explain complex features simply
        - If implementation comes up, transfer to Customer Success
        - For general support, transfer to Support Agent
        - Keep responses under 50 words
        Focus on API capabilities, integrations, and security features.""",
        functions=[
            system.transfer_to_success,
            system.transfer_to_support,
            system.transfer_to_sales
        ]
    )
    
    # Customer Success
    agents["success"] = Agent(
        name="Customer Success",
        instructions="""You are a customer success manager focused on implementation.
        - Share implementation best practices
        - If technical issues arise, transfer to Technical Agent
        - For pricing questions, transfer to Sales
        - Keep responses under 50 words
        Focus on onboarding, training, and optimization.""",
        functions=[
            system.transfer_to_technical,
            system.transfer_to_sales,
            system.schedule_demo
        ]
    )
    
    # Support Agent
    agents["support"] = Agent(
        name="Support Agent",
        instructions="""You are a technical support specialist.
        - Provide step-by-step guidance
        - For deep technical issues, transfer to Technical Agent
        - For billing issues, transfer to Billing Agent
        - Keep responses under 50 words
        24/7 support for premium tier, business hours for standard.""",
        functions=[
            system.transfer_to_technical,
            system.transfer_to_billing,
            system.escalate_issue
        ]
    )
    
    # Billing Agent
# Billing Agent (continued)
    agents["billing"] = Agent(
        name="Billing Agent",
        instructions="""You are a billing department representative.
        - Handle payment and billing inquiries
        - For plan upgrades, transfer to Sales
        - For technical issues, transfer to Support
        - Keep responses under 50 words
        Handle monthly/annual billing, volume discounts.""",
        functions=[
            system.transfer_to_sales,
            system.transfer_to_support,
            system.process_upgrade
        ]
    )
    
    # Receptionist
    agents["receptionist"] = Agent(
        name="Receptionist",
        instructions="""You are a friendly corporate receptionist.
        - Understand customer needs thoroughly before transferring
        - Can transfer to any department based on needs
        - Keep responses under 40 words
        - Ask clarifying questions before transfer
        Guide conversations to the right specialist.""",
        functions=[
            system.transfer_to_sales,
            system.transfer_to_support,
            system.transfer_to_billing,
            system.transfer_to_technical,
            system.transfer_to_success,
            system.assess_needs
        ]
    )
    
    return agents

# Transfer functions
def transfer_to_technical(self):
    """Transfer to technical agent with context"""
    return self.technical_agent

def transfer_to_success(self):
    """Transfer to customer success with context"""
    return self.customer_success

def transfer_to_sales(self):
    """Transfer to sales with context"""
    return self.sales_agent

def transfer_to_support(self):
    """Transfer to support with context"""
    return self.support_agent

def transfer_to_billing(self):
    """Transfer to billing with context"""
    return self.billing_agent

# Additional interaction functions
def check_customer_fit(self):
    """Analyze if customer needs align with product"""
    print("Analyzing customer fit...")
    return "Analyzing customer requirements for best solution fit."

def schedule_demo(self):
    """Schedule a product demonstration"""
    print("Scheduling demo...")
    return "I can help schedule a demonstration of our platform."

def escalate_issue(self):
    """Escalate support issue to higher tier"""
    print("Escalating issue...")
    return "I'll escalate this to our senior support team."

def process_upgrade(self):
    """Handle plan upgrade request"""
    print("Processing upgrade...")
    return "I can help process your plan upgrade."

def assess_needs(self):
    """Detailed needs assessment"""
    print("Assessing needs...")
    return "Let me understand your requirements better."

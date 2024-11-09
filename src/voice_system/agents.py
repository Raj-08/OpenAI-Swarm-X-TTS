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
    agents["billing"] = Agent(
        name="Billing Agent",

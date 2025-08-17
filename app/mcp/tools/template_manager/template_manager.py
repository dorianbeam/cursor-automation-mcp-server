# app/mcp/tools/template_manager/template_manager.py
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import time

from app.mcp.server import mcp
from pydantic import BaseModel, Field

class TemplateInfo(BaseModel):
    """Information about a single template"""
    name: str = Field(..., description="Template identifier")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="What this template creates")
    category: str = Field(..., description="Template category")
    complexity: str = Field(..., description="Basic, Intermediate, or Advanced")
    build_time: str = Field(..., description="Estimated build time")
    success_rate: str = Field(..., description="Historical success rate")
    use_cases: List[str] = Field(..., description="Common use cases")
    capabilities: List[str] = Field(..., description="Built-in capabilities")
    enhancements: List[str] = Field(..., description="Available enhancements")
    created_date: str = Field(..., description="When template was created")
    usage_count: int = Field(..., description="Number of times used")

class TemplateListInput(BaseModel):
    """Input for listing templates"""
    category: Optional[str] = Field(
        None,
        description="Filter by category: data_processing, api_integration, web_automation, workflow, document_processing"
    )
    complexity: Optional[str] = Field(
        None, 
        description="Filter by complexity: basic, intermediate, advanced"
    )
    sort_by: str = Field(
        "popularity",
        description="Sort by: popularity, name, success_rate, build_time, created_date"
    )

class TemplateDetailsInput(BaseModel):
    """Input for getting template details"""
    template_name: str = Field(..., description="Name of the template to get details for")
    include_usage_examples: bool = Field(True, description="Include usage examples and code snippets")

class TemplateUsageExample(BaseModel):
    """Usage example for a template"""
    scenario: str = Field(..., description="Usage scenario")
    description: str = Field(..., description="What this example demonstrates")
    configuration: Dict[str, Any] = Field(..., description="Example configuration")
    expected_output: str = Field(..., description="What the template would generate")

class TemplateDetailsOutput(BaseModel):
    """Detailed information about a template"""
    template: TemplateInfo = Field(..., description="Template information")
    implementation_details: Dict[str, Any] = Field(..., description="Technical implementation details")
    usage_examples: List[TemplateUsageExample] = Field(..., description="Usage examples")
    customization_options: List[str] = Field(..., description="Available customization options")
    prerequisites: List[str] = Field(..., description="Prerequisites for using this template")
    related_templates: List[str] = Field(..., description="Other templates that work well with this one")

class TemplateListOutput(BaseModel):
    """Output from listing templates"""
    templates: List[TemplateInfo] = Field(..., description="List of templates matching criteria")
    total_count: int = Field(..., description="Total number of templates available")
    filtered_count: int = Field(..., description="Number of templates matching filters")
    categories_available: List[str] = Field(..., description="All available categories")

class TemplateCreationInput(BaseModel):
    """Input for creating a custom template"""
    template_name: str = Field(..., description="Name for the new template")
    description: str = Field(..., description="Description of what this template creates")
    category: str = Field(..., description="Template category")
    base_template: Optional[str] = Field(None, description="Existing template to base this on")
    customizations: Dict[str, Any] = Field(..., description="Specific customizations for this template")
    capabilities: List[str] = Field(..., description="Required capabilities")
    enhancements: List[str] = Field(default=[], description="Additional enhancements to include")

class TemplateCreationOutput(BaseModel):
    """Output from creating a template"""
    success: bool = Field(..., description="Whether template was created successfully")
    template_name: str = Field(..., description="Name of the created template")
    template_location: str = Field(..., description="Where the template files are stored")
    usage_instructions: str = Field(..., description="How to use the new template")
    validation_results: List[str] = Field(..., description="Template validation results")

@mcp.tool(
    description="List all available automation templates with filtering and sorting options."
)
async def list_templates(input_data: TemplateListInput) -> TemplateListOutput:
    """
    List all available automation templates with comprehensive filtering options.
    
    Templates are proven automation patterns that provide:
    - Faster system creation with higher success rates
    - Built-in best practices and error handling
    - Professional features and enhancements
    - Customization options for specific needs
    
    Use filters to find templates that match your specific requirements.
    """
    
    # Get all available templates
    all_templates = await _load_all_templates()
    
    # Apply filters
    filtered_templates = _apply_template_filters(
        all_templates, 
        input_data.category, 
        input_data.complexity
    )
    
    # Sort templates
    sorted_templates = _sort_templates(filtered_templates, input_data.sort_by)
    
    # Get available categories
    categories = list(set(template.category for template in all_templates))
    
    return TemplateListOutput(
        templates=sorted_templates,
        total_count=len(all_templates),
        filtered_count=len(sorted_templates),
        categories_available=categories
    )

@mcp.tool(
    description="Get detailed information about a specific template including usage examples and customization options."
)
async def get_template_details(input_data: TemplateDetailsInput) -> TemplateDetailsOutput:
    """
    Get comprehensive details about a specific automation template.
    
    This provides:
    - Complete template specifications and capabilities
    - Usage examples with different configurations
    - Customization options and prerequisites
    - Related templates that work well together
    - Implementation details for advanced users
    
    Use this to understand exactly what a template provides before building.
    """
    
    # Load the specific template
    template = await _load_template_by_name(input_data.template_name)
    if not template:
        raise ValueError(f"Template '{input_data.template_name}' not found")
    
    # Get implementation details
    impl_details = await _get_template_implementation(input_data.template_name)
    
    # Generate usage examples if requested
    usage_examples = []
    if input_data.include_usage_examples:
        usage_examples = await _generate_template_examples(input_data.template_name)
    
    # Get customization options
    customizations = await _get_template_customizations(input_data.template_name)
    
    # Find related templates
    related = await _find_related_templates(input_data.template_name, template.category)
    
    return TemplateDetailsOutput(
        template=template,
        implementation_details=impl_details,
        usage_examples=usage_examples,
        customization_options=customizations,
        prerequisites=impl_details.get("prerequisites", []),
        related_templates=related
    )

@mcp.tool(
    description="Create a custom template from specifications or by customizing an existing template."
)
async def create_custom_template(input_data: TemplateCreationInput) -> TemplateCreationOutput:
    """
    Create a custom automation template for reuse.
    
    Custom templates enable:
    - Standardization of your specific automation patterns
    - Faster creation of similar systems
    - Sharing proven patterns across teams
    - Building organization-specific automation libraries
    
    Templates can be created from scratch or by customizing existing templates.
    """
    
    # Validate template name
    if await _template_exists(input_data.template_name):
        raise ValueError(f"Template '{input_data.template_name}' already exists")
    
    # Create the template
    creation_result = await _create_template(input_data)
    
    # Validate the created template
    validation_results = await _validate_template(input_data.template_name)
    
    return TemplateCreationOutput(
        success=creation_result["success"],
        template_name=input_data.template_name,
        template_location=creation_result["location"],
        usage_instructions=creation_result["instructions"],
        validation_results=validation_results
    )

# Helper functions for template management

async def _load_all_templates() -> List[TemplateInfo]:
    """Load all available templates from the framework"""
    
    templates = []
    
    # Built-in templates
    built_in_templates = [
        {
            "name": "data_processor",
            "display_name": "Data Processing System", 
            "description": "Multi-format data processor with validation, transformation, and professional reporting",
            "category": "data_processing",
            "complexity": "Intermediate",
            "build_time": "8-12 minutes",
            "success_rate": "95%",
            "use_cases": ["CSV processing", "Excel analysis", "Data validation", "Report generation", "ETL pipelines"],
            "capabilities": ["file_reading", "data_validation", "transformation", "reporting", "error_handling"],
            "enhancements": ["streaming_support", "advanced_validation", "performance_optimization", "cloud_integration"],
            "created_date": "2024-01-01",
            "usage_count": 127
        },
        {
            "name": "api_integrator",
            "display_name": "API Integration System",
            "description": "Bi-directional API synchronization with rate limiting, error recovery, and data transformation",
            "category": "api_integration", 
            "complexity": "Advanced",
            "build_time": "12-18 minutes",
            "success_rate": "92%",
            "use_cases": ["CRM synchronization", "Data pipelines", "System integration", "Webhook processing", "Real-time sync"],
            "capabilities": ["authentication", "request_handling", "data_transformation", "sync_verification", "error_recovery"],
            "enhancements": ["rate_limiting", "retry_logic", "monitoring", "conflict_resolution", "audit_logging"],
            "created_date": "2024-01-05",
            "usage_count": 89
        },
        {
            "name": "web_automator",
            "display_name": "Web Automation System",
            "description": "Browser automation with monitoring, data extraction, and form processing capabilities",
            "category": "web_automation",
            "complexity": "Advanced", 
            "build_time": "15-20 minutes",
            "success_rate": "88%",
            "use_cases": ["Website monitoring", "Data scraping", "Form automation", "Change detection", "Content extraction"],
            "capabilities": ["browser_control", "element_interaction", "data_extraction", "monitoring", "scheduling"],
            "enhancements": ["proxy_support", "captcha_handling", "error_recovery", "parallel_processing", "cloud_deployment"],
            "created_date": "2024-01-10",
            "usage_count": 64
        },
        {
            "name": "workflow_engine",
            "display_name": "Workflow Automation Engine",
            "description": "Task scheduling and process orchestration with team collaboration features",
            "category": "workflow",
            "complexity": "Basic",
            "build_time": "6-10 minutes", 
            "success_rate": "97%",
            "use_cases": ["Daily reports", "Batch processing", "Event-driven tasks", "Team workflows", "Scheduled operations"],
            "capabilities": ["task_scheduling", "event_handling", "process_orchestration", "notifications", "monitoring"],
            "enhancements": ["advanced_scheduling", "team_collaboration", "analytics", "alerting", "integration_hooks"],
            "created_date": "2024-01-03",
            "usage_count": 156
        },
        {
            "name": "document_processor",
            "display_name": "Document Processing System",
            "description": "Content analysis, document automation, and intelligent categorization system",
            "category": "document_processing",
            "complexity": "Intermediate",
            "build_time": "10-14 minutes",
            "success_rate": "93%",
            "use_cases": ["PDF processing", "Content extraction", "Document classification", "Text analysis", "Format conversion"],
            "capabilities": ["text_extraction", "content_analysis", "format_conversion", "classification", "metadata_extraction"],
            "enhancements": ["ai_analysis", "batch_processing", "cloud_integration", "security", "version_control"],
            "created_date": "2024-01-07",
            "usage_count": 78
        }
    ]
    
    # Convert to TemplateInfo objects
    for template_data in built_in_templates:
        templates.append(TemplateInfo(**template_data))
    
    # Load custom templates from filesystem
    custom_templates = await _load_custom_templates()
    templates.extend(custom_templates)
    
    return templates

async def _load_custom_templates() -> List[TemplateInfo]:
    """Load custom templates from the templates directory"""
    
    templates = []
    templates_dir = Path("automation-systems/automation-framework/templates")
    
    if not templates_dir.exists():
        return templates
    
    # Look for custom template files
    for template_file in templates_dir.glob("*.json"):
        try:
            with open(template_file, 'r') as f:
                template_data = json.load(f)
                
            # Convert to TemplateInfo if it has the required fields
            if all(key in template_data for key in ["name", "display_name", "description"]):
                # Fill in missing fields with defaults
                template_info = {
                    "category": template_data.get("category", "custom"),
                    "complexity": template_data.get("complexity", "Intermediate"),
                    "build_time": template_data.get("build_time", "10-15 minutes"),
                    "success_rate": template_data.get("success_rate", "90%"),
                    "use_cases": template_data.get("use_cases", ["Custom automation"]),
                    "capabilities": template_data.get("capabilities", ["custom_processing"]),
                    "enhancements": template_data.get("enhancements", ["error_handling"]),
                    "created_date": template_data.get("created_date", "2024-01-01"),
                    "usage_count": template_data.get("usage_count", 0),
                    **template_data
                }
                
                templates.append(TemplateInfo(**template_info))
                
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            # Skip invalid template files
            continue
    
    return templates

def _apply_template_filters(templates: List[TemplateInfo], category: Optional[str], complexity: Optional[str]) -> List[TemplateInfo]:
    """Apply filters to template list"""
    
    filtered = templates
    
    if category:
        filtered = [t for t in filtered if t.category.lower() == category.lower()]
    
    if complexity:
        filtered = [t for t in filtered if t.complexity.lower() == complexity.lower()]
    
    return filtered

def _sort_templates(templates: List[TemplateInfo], sort_by: str) -> List[TemplateInfo]:
    """Sort templates by specified criteria"""
    
    if sort_by == "popularity":
        return sorted(templates, key=lambda t: t.usage_count, reverse=True)
    elif sort_by == "name":
        return sorted(templates, key=lambda t: t.display_name)
    elif sort_by == "success_rate":
        # Extract numeric value from success rate string
        return sorted(templates, key=lambda t: float(t.success_rate.rstrip('%')), reverse=True)
    elif sort_by == "build_time":
        # Extract first number from build time string for sorting
        return sorted(templates, key=lambda t: int(t.build_time.split('-')[0]))
    elif sort_by == "created_date":
        return sorted(templates, key=lambda t: t.created_date, reverse=True)
    else:
        return templates

async def _load_template_by_name(template_name: str) -> Optional[TemplateInfo]:
    """Load a specific template by name"""
    
    all_templates = await _load_all_templates()
    return next((t for t in all_templates if t.name == template_name), None)

async def _get_template_implementation(template_name: str) -> Dict[str, Any]:
    """Get implementation details for a template"""
    
    implementation_details = {
        "data_processor": {
            "architecture": "Modular data processing pipeline",
            "dependencies": ["pandas", "numpy", "openpyxl", "matplotlib"],
            "file_structure": ["main.py", "processors/", "validators/", "reporters/", "config/"],
            "entry_point": "main.py",
            "configuration_files": ["config.json", "validation_rules.json"],
            "prerequisites": ["Python 3.8+", "Basic data processing knowledge"],
            "performance_characteristics": "Handles up to 1M records efficiently",
            "scaling_options": "Horizontal scaling via batch processing"
        },
        "api_integrator": {
            "architecture": "Event-driven API synchronization system", 
            "dependencies": ["httpx", "pydantic", "asyncio", "tenacity"],
            "file_structure": ["main.py", "integrations/", "transformers/", "auth/", "config/"],
            "entry_point": "main.py",
            "configuration_files": ["api_config.json", "mapping_rules.json"],
            "prerequisites": ["API documentation", "Authentication credentials", "Data mapping knowledge"],
            "performance_characteristics": "Handles 1000+ API calls per minute",
            "scaling_options": "Async processing, rate limiting, queue management"
        },
        "web_automator": {
            "architecture": "Headless browser automation framework",
            "dependencies": ["selenium", "beautifulsoup4", "requests", "schedule"],
            "file_structure": ["main.py", "scrapers/", "monitors/", "extractors/", "config/"],
            "entry_point": "main.py", 
            "configuration_files": ["sites_config.json", "extraction_rules.json"],
            "prerequisites": ["Chrome/Firefox browser", "Web scraping knowledge", "CSS/XPath basics"],
            "performance_characteristics": "Processes multiple sites concurrently",
            "scaling_options": "Parallel browser instances, proxy rotation"
        },
        "workflow_engine": {
            "architecture": "Cron-based task orchestration system",
            "dependencies": ["schedule", "sqlite3", "logging", "smtplib"],
            "file_structure": ["main.py", "tasks/", "schedulers/", "notifications/", "storage/"],
            "entry_point": "main.py",
            "configuration_files": ["schedule_config.json", "notification_settings.json"],
            "prerequisites": ["Task definitions", "Schedule requirements"],
            "performance_characteristics": "Manages hundreds of scheduled tasks",
            "scaling_options": "Distributed scheduling, task queues"
        },
        "document_processor": {
            "architecture": "Multi-format document processing pipeline", 
            "dependencies": ["PyPDF2", "python-docx", "openpyxl", "nltk"],
            "file_structure": ["main.py", "extractors/", "analyzers/", "converters/", "config/"],
            "entry_point": "main.py",
            "configuration_files": ["document_types.json", "analysis_rules.json"],
            "prerequisites": ["Document samples", "Processing requirements"],
            "performance_characteristics": "Processes documents of various sizes",
            "scaling_options": "Batch processing, cloud storage integration"
        }
    }
    
    return implementation_details.get(template_name, {
        "architecture": "Custom automation system",
        "dependencies": ["Standard Python libraries"],
        "file_structure": ["main.py", "config.json"],
        "entry_point": "main.py",
        "prerequisites": ["Python 3.8+"],
        "performance_characteristics": "Varies based on implementation",
        "scaling_options": "Depends on specific requirements"
    })

async def _generate_template_examples(template_name: str) -> List[TemplateUsageExample]:
    """Generate usage examples for a template"""
    
    examples_map = {
        "data_processor": [
            TemplateUsageExample(
                scenario="Sales Data Analysis",
                description="Process monthly sales CSV files and generate executive reports",
                configuration={
                    "input_files": ["sales_jan.csv", "sales_feb.csv", "sales_mar.csv"],
                    "validation_rules": {"required_columns": ["date", "amount", "customer"]},
                    "report_format": "executive_summary",
                    "output_format": ["pdf", "excel"]
                },
                expected_output="Professional sales analysis report with charts, trends, and key metrics"
            ),
            TemplateUsageExample(
                scenario="Customer Data Cleanup",
                description="Clean and validate customer data from multiple sources",
                configuration={
                    "input_sources": ["crm_export.csv", "website_signups.json"],
                    "validation_rules": {"email_validation": True, "phone_cleanup": True},
                    "deduplication": {"match_fields": ["email", "phone"]},
                    "output_format": "cleaned_customers.csv"
                },
                expected_output="Cleaned, validated customer database with duplicates removed"
            )
        ],
        "api_integrator": [
            TemplateUsageExample(
                scenario="CRM to Marketing Platform Sync",
                description="Synchronize customer data between CRM and marketing automation platform",
                configuration={
                    "source_api": {"type": "salesforce", "endpoint": "contacts"},
                    "target_api": {"type": "hubspot", "endpoint": "contacts"},
                    "sync_frequency": "hourly",
                    "field_mapping": {"sf_email": "hs_email", "sf_company": "hs_company"}
                },
                expected_output="Automated bi-directional sync keeping both systems updated"
            )
        ],
        "web_automator": [
            TemplateUsageExample(
                scenario="E-commerce Price Monitoring", 
                description="Monitor competitor prices and send alerts when changes occur",
                configuration={
                    "target_sites": ["competitor1.com/product", "competitor2.com/product"],
                    "check_frequency": "daily",
                    "price_selectors": {".price", ".cost", "[data-price]"},
                    "alert_threshold": "5%"
                },
                expected_output="Daily price monitoring with email alerts for significant changes"
            )
        ],
        "workflow_engine": [
            TemplateUsageExample(
                scenario="Daily Report Generation",
                description="Generate and distribute daily business reports to stakeholders",
                configuration={
                    "schedule": "daily at 8:00 AM",
                    "data_sources": ["database", "api_endpoints", "csv_files"],
                    "report_types": ["sales_summary", "inventory_status"],
                    "distribution": {"email": ["manager@company.com"], "slack": "#reports"}
                },
                expected_output="Automated daily reports delivered to team via email and Slack"
            )
        ],
        "document_processor": [
            TemplateUsageExample(
                scenario="Contract Analysis",
                description="Extract key information from legal contracts and categorize by type",
                configuration={
                    "input_directory": "/contracts/pending",
                    "extraction_fields": ["parties", "terms", "dates", "amounts"],
                    "classification_rules": "contract_types.json",
                    "output_format": "structured_data.json"
                },
                expected_output="Structured contract data with key terms extracted and categorized"
            )
        ]
    }
    
    return examples_map.get(template_name, [
        TemplateUsageExample(
            scenario="Basic Usage",
            description="Standard template usage pattern",
            configuration={"input": "data", "output": "processed_data"},
            expected_output="Processed automation system"
        )
    ])

async def _get_template_customizations(template_name: str) -> List[str]:
    """Get available customization options for a template"""
    
    customizations_map = {
        "data_processor": [
            "Custom validation rules and data quality checks",
            "Additional input/output formats (JSON, XML, Parquet)",
            "Custom reporting templates and chart types",
            "Integration with specific databases or cloud services",
            "Custom transformation functions and business logic",
            "Advanced scheduling and automation options"
        ],
        "api_integrator": [
            "Custom authentication methods (OAuth, JWT, API keys)",
            "Specific API endpoint configurations",
            "Custom data transformation rules",
            "Rate limiting and retry strategies",
            "Webhook processing and event handling",
            "Custom monitoring and alerting rules"
        ],
        "web_automator": [
            "Site-specific extraction rules and selectors",
            "Custom browser configurations and proxy settings", 
            "JavaScript rendering and SPA support",
            "Custom scheduling and monitoring frequencies",
            "Data cleaning and transformation rules",
            "Integration with data storage systems"
        ],
        "workflow_engine": [
            "Custom task definitions and execution logic",
            "Advanced scheduling patterns (cron, event-based)",
            "Custom notification channels and formatting",
            "Integration with external systems and APIs",
            "Custom error handling and recovery strategies",
            "Team collaboration and approval workflows"
        ],
        "document_processor": [
            "Custom document type recognition rules",
            "Specific extraction patterns and field definitions",
            "Custom analysis and classification logic",
            "Integration with document management systems",
            "Custom output formats and templates", 
            "OCR and image processing capabilities"
        ]
    }
    
    return customizations_map.get(template_name, [
        "Basic configuration customization",
        "Input/output format options",
        "Custom processing logic",
        "Integration options"
    ])

async def _find_related_templates(template_name: str, category: str) -> List[str]:
    """Find templates that work well with the given template"""
    
    all_templates = await _load_all_templates()
    
    related = []
    
    # Templates in the same category
    same_category = [t.name for t in all_templates if t.category == category and t.name != template_name]
    related.extend(same_category[:2])  # Limit to 2 from same category
    
    # Complementary templates based on common workflows
    complementary_map = {
        "data_processor": ["api_integrator", "workflow_engine"],
        "api_integrator": ["data_processor", "document_processor"],
        "web_automator": ["data_processor", "workflow_engine"], 
        "workflow_engine": ["data_processor", "api_integrator"],
        "document_processor": ["data_processor", "workflow_engine"]
    }
    
    if template_name in complementary_map:
        for comp_name in complementary_map[template_name]:
            if comp_name not in related:
                related.append(comp_name)
    
    return related[:4]  # Limit to 4 related templates

async def _template_exists(template_name: str) -> bool:
    """Check if a template with the given name already exists"""
    
    all_templates = await _load_all_templates()
    return any(t.name == template_name for t in all_templates)

async def _create_template(input_data: TemplateCreationInput) -> Dict[str, Any]:
    """Create a new custom template"""
    
    # Create template directory
    templates_dir = Path("automation-systems/automation-framework/templates")
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Create template metadata
    template_metadata = {
        "name": input_data.template_name,
        "display_name": input_data.template_name.replace("_", " ").title(),
        "description": input_data.description,
        "category": input_data.category,
        "complexity": "Custom",
        "build_time": "10-15 minutes",
        "success_rate": "90%",
        "use_cases": ["Custom automation based on specific requirements"],
        "capabilities": input_data.capabilities,
        "enhancements": input_data.enhancements,
        "created_date": time.strftime("%Y-%m-%d"),
        "usage_count": 0,
        "customizations": input_data.customizations,
        "base_template": input_data.base_template,
        "template_version": "1.0.0"
    }
    
    # Save template metadata
    template_file = templates_dir / f"{input_data.template_name}.json"
    with open(template_file, 'w') as f:
        json.dump(template_metadata, f, indent=2)
    
    return {
        "success": True,
        "location": str(template_file),
        "instructions": f"Template '{input_data.template_name}' created successfully. Use 'build_from_template' with template_name='{input_data.template_name}' to build systems from this template."
    }

async def _validate_template(template_name: str) -> List[str]:
    """Validate a template for completeness and correctness"""
    
    validation_results = []
    
    # Check if template file exists
    template_file = Path(f"automation-systems/automation-framework/templates/{template_name}.json")
    if not template_file.exists():
        validation_results.append("❌ Template file not found")
        return validation_results
    
    # Load and validate template structure
    try:
        with open(template_file, 'r') as f:
            template_data = json.load(f)
        
        required_fields = ["name", "display_name", "description", "category", "capabilities"]
        missing_fields = [field for field in required_fields if field not in template_data]
        
        if missing_fields:
            validation_results.append(f"❌ Missing required fields: {', '.join(missing_fields)}")
        else:
            validation_results.append("✅ All required fields present")
        
        if template_data.get("capabilities") and len(template_data["capabilities"]) > 0:
            validation_results.append("✅ Template has defined capabilities")
        else:
            validation_results.append("⚠️ No capabilities defined")
        
        if template_data.get("description") and len(template_data["description"]) > 20:
            validation_results.append("✅ Good description provided")
        else:
            validation_results.append("⚠️ Description could be more detailed")
            
    except json.JSONDecodeError:
        validation_results.append("❌ Invalid JSON format in template file")
    except Exception as e:
        validation_results.append(f"❌ Error validating template: {str(e)}")
    
    return validation_results
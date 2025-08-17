# app/mcp/tools/automation_builder/automation_builder_pydantic.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class BuildMode(str, Enum):
    BUILD = "BUILD_MODE"
    LEARN = "LEARN_MODE" 
    BALANCED = "BALANCED"
    AUTO_DETECT = "AUTO_DETECT"

class SystemType(str, Enum):
    DATA_PROCESSING = "data_processing"
    API_INTEGRATION = "api_integration"
    WEB_AUTOMATION = "web_automation"
    WORKFLOW_AUTOMATION = "workflow_automation"
    DOCUMENT_PROCESSING = "document_processing"
    CUSTOM = "custom"

class EnhancementPreference(str, Enum):
    AUTOMATIC = "automatic"          # Apply all beneficial enhancements
    ASK_MAJOR = "ask_major"         # Ask for major enhancements only
    ASK_ALL = "ask_all"             # Ask before any enhancements
    MINIMAL = "minimal"             # No enhancements, basic system only

class AutomationBuilderInput(BaseModel):
    """Input for building an automation system"""
    
    automation_goal: str = Field(
        ..., 
        description="What you want to automate (e.g., 'Process CSV files and generate reports', 'Sync data between APIs', 'Monitor websites for changes')"
    )
    
    system_type: Optional[SystemType] = Field(
        None,
        description="Type of automation system to build. If not specified, will be auto-detected from the goal."
    )
    
    build_mode: BuildMode = Field(
        BuildMode.AUTO_DETECT,
        description="How to approach the building process: BUILD_MODE (efficiency), LEARN_MODE (educational), BALANCED (adaptive), or AUTO_DETECT (determine from context)"
    )
    
    enhancement_preference: EnhancementPreference = Field(
        EnhancementPreference.ASK_MAJOR,
        description="How to handle enhancement suggestions: automatic, ask_major, ask_all, or minimal"
    )
    
    workspace_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context about workspace files, APIs, or existing systems that should influence the build"
    )
    
    custom_requirements: Optional[List[str]] = Field(
        None,
        description="Specific requirements or constraints for the automation system"
    )

class SystemCapability(BaseModel):
    """Describes a capability of the built system"""
    name: str = Field(..., description="Name of the capability")
    description: str = Field(..., description="What this capability does")
    auto_applied: bool = Field(..., description="Whether this was automatically applied")

class EnhancementSuggestion(BaseModel):
    """An enhancement that could be added to the system"""
    name: str = Field(..., description="Name of the enhancement")
    description: str = Field(..., description="What this enhancement provides")
    benefit: str = Field(..., description="Why this enhancement is valuable")
    time_estimate: str = Field(..., description="Estimated time to implement")
    recommended: bool = Field(..., description="Whether this is strongly recommended")

class BuildProgress(BaseModel):
    """Progress information during system building"""
    phase: str = Field(..., description="Current build phase")
    progress_percent: int = Field(..., description="Progress percentage (0-100)")
    current_activity: str = Field(..., description="What's currently being built")
    time_estimate: str = Field(..., description="Estimated time remaining")

class AutomationBuilderOutput(BaseModel):
    """Output from building an automation system"""
    
    success: bool = Field(..., description="Whether the system was built successfully")
    
    system_name: str = Field(..., description="Name of the built automation system")
    
    system_description: str = Field(..., description="Description of what the system does")
    
    capabilities: List[SystemCapability] = Field(
        ..., 
        description="List of capabilities built into the system"
    )
    
    file_locations: Dict[str, str] = Field(
        ..., 
        description="Key files created and their purposes"
    )
    
    usage_instructions: str = Field(
        ..., 
        description="How to use the built automation system"
    )
    
    build_time_minutes: float = Field(
        ..., 
        description="Actual time taken to build the system"
    )
    
    applied_enhancements: List[str] = Field(
        ..., 
        description="Enhancements that were automatically applied"
    )
    
    suggested_enhancements: List[EnhancementSuggestion] = Field(
        default=[],
        description="Additional enhancements that could be added"
    )
    
    performance_metrics: Dict[str, Any] = Field(
        default={},
        description="Expected performance characteristics of the built system"
    )
    
    next_steps: List[str] = Field(
        default=[],
        description="Recommended next actions to take with the system"
    )
    
    template_generated: Optional[str] = Field(
        None,
        description="If this build was successful enough to generate a reusable template, the template name"
    )

# Template-specific models
class TemplateBuilderInput(BaseModel):
    """Input for building from a specific template"""
    
    template_name: str = Field(
        ..., 
        description="Name of the template to use (e.g., 'data_processor', 'api_sync', 'web_monitor')"
    )
    
    customizations: Optional[Dict[str, Any]] = Field(
        None,
        description="Specific customizations to apply to the template"
    )
    
    build_mode: BuildMode = Field(
        BuildMode.AUTO_DETECT,
        description="Building approach mode"
    )

class AvailableTemplate(BaseModel):
    """Information about an available template"""
    name: str = Field(..., description="Template identifier")
    display_name: str = Field(..., description="Human-readable template name")
    description: str = Field(..., description="What this template creates")
    use_cases: List[str] = Field(..., description="Common use cases for this template")
    build_time: str = Field(..., description="Estimated build time")
    complexity: str = Field(..., description="Complexity level (Basic, Intermediate, Advanced)")
    success_rate: str = Field(..., description="Success rate percentage")

class TemplateListOutput(BaseModel):
    """Output listing available templates"""
    templates: List[AvailableTemplate] = Field(..., description="Available automation templates")
    total_count: int = Field(..., description="Total number of templates available")

# Learning system models
class LearningPathInput(BaseModel):
    """Input for starting a learning path"""
    
    topic: str = Field(
        ..., 
        description="What you want to learn (e.g., 'data processing', 'API integration', 'automation basics')"
    )
    
    skill_level: Optional[str] = Field(
        "beginner",
        description="Your current skill level: beginner, intermediate, advanced"
    )
    
    learning_style: Optional[str] = Field(
        "hands_on",
        description="Preferred learning style: hands_on, tutorial, guided, reference"
    )

class LearningStep(BaseModel):
    """A step in a learning path"""
    step_number: int = Field(..., description="Step number in the sequence")
    title: str = Field(..., description="Title of this learning step")
    description: str = Field(..., description="What you'll learn in this step")
    estimated_time: str = Field(..., description="Estimated time for this step")
    hands_on_component: bool = Field(..., description="Whether this step includes building something")

class LearningPathOutput(BaseModel):
    """Output for a learning path"""
    path_name: str = Field(..., description="Name of the learning path")
    total_steps: int = Field(..., description="Total number of steps")
    estimated_duration: str = Field(..., description="Total estimated time")
    steps: List[LearningStep] = Field(..., description="The learning steps")
    prerequisites: List[str] = Field(default=[], description="Prerequisites for this path")
    outcomes: List[str] = Field(..., description="What you'll be able to do after completing this path")

# Meta-optimization models
class MetaOptimizationInput(BaseModel):
    """Input for meta-optimization analysis"""
    
    focus_area: Optional[str] = Field(
        None,
        description="Specific area to optimize (e.g., 'build_speed', 'user_experience', 'system_performance'). If not specified, analyzes all areas."
    )
    
    include_suggestions: bool = Field(
        True,
        description="Whether to include specific optimization suggestions"
    )

class OptimizationOpportunity(BaseModel):
    """An identified optimization opportunity"""
    area: str = Field(..., description="Area that can be optimized")
    current_performance: str = Field(..., description="Current performance level")
    target_performance: str = Field(..., description="Target performance level") 
    method: str = Field(..., description="How to implement this optimization")
    expected_improvement: str = Field(..., description="Expected improvement from this optimization")
    effort_level: str = Field(..., description="Implementation effort: Low, Medium, High")

class MetaOptimizationOutput(BaseModel):
    """Output from meta-optimization analysis"""
    
    current_system_health: str = Field(..., description="Overall assessment of current system performance")
    
    performance_metrics: Dict[str, str] = Field(
        ..., 
        description="Current performance in key areas"
    )
    
    optimization_opportunities: List[OptimizationOpportunity] = Field(
        ..., 
        description="Identified opportunities for improvement"
    )
    
    priority_optimizations: List[str] = Field(
        ..., 
        description="Top priority optimizations that should be implemented first"
    )
    
    system_evolution_suggestions: List[str] = Field(
        default=[],
        description="Suggestions for evolving the system's capabilities"
    )
# app/mcp/tools/workspace_analyzer/workspace_analyzer.py
import os
from pathlib import Path
from typing import Dict, List, Any
import json

from app.mcp.server import mcp
from pydantic import BaseModel, Field

class WorkspaceAnalysisInput(BaseModel):
    """Input for workspace analysis"""
    target_directory: str = Field(
        ".",
        description="Directory to analyze (default: current directory)"
    )
    analysis_depth: str = Field(
        "standard",
        description="Analysis depth: shallow, standard, or deep"
    )
    include_suggestions: bool = Field(
        True,
        description="Whether to include automation suggestions based on findings"
    )

class FilePattern(BaseModel):
    """Information about discovered file patterns"""
    pattern_type: str = Field(..., description="Type of files found")
    file_count: int = Field(..., description="Number of matching files")
    total_size_mb: float = Field(..., description="Total size in MB")
    examples: List[str] = Field(..., description="Example file paths")
    automation_opportunity: str = Field(..., description="What could be automated with these files")

class AutomationSuggestion(BaseModel):
    """Suggested automation based on workspace analysis"""
    automation_type: str = Field(..., description="Type of automation suggested")
    description: str = Field(..., description="What this automation would do")
    confidence: str = Field(..., description="Confidence level: High, Medium, Low")
    estimated_value: str = Field(..., description="Expected value/time savings")
    files_involved: List[str] = Field(..., description="Files that would be processed")

class WorkspaceAnalysisOutput(BaseModel):
    """Output from workspace analysis"""
    analysis_summary: str = Field(..., description="High-level summary of the workspace")
    file_patterns: List[FilePattern] = Field(..., description="Discovered file patterns")
    automation_suggestions: List[AutomationSuggestion] = Field(..., description="Recommended automations")
    integration_opportunities: List[str] = Field(..., description="Detected integration opportunities")
    total_files_analyzed: int = Field(..., description="Total number of files analyzed")
    workspace_health_score: str = Field(..., description="Overall workspace organization score")

@mcp.tool(
    description="Analyze a workspace to identify automation opportunities, file patterns, and integration possibilities."
)
async def analyze_workspace(input_data: WorkspaceAnalysisInput) -> WorkspaceAnalysisOutput:
    """
    Perform intelligent workspace analysis to discover automation opportunities.
    
    This tool scans the specified directory and identifies:
    - Data files that could be processed automatically
    - API documentation suggesting integration opportunities
    - Repetitive file patterns that could be automated
    - Configuration files indicating system integrations
    - Templates and schemas for report automation
    
    The analysis provides specific automation suggestions with confidence levels
    and estimated value, making it easy to prioritize automation projects.
    """
    
    target_path = Path(input_data.target_directory)
    if not target_path.exists():
        raise ValueError(f"Directory '{input_data.target_directory}' does not exist")
    
    # Perform the analysis
    analysis = await _perform_workspace_analysis(target_path, input_data.analysis_depth)
    
    # Generate automation suggestions if requested
    suggestions = []
    if input_data.include_suggestions:
        suggestions = await _generate_automation_suggestions(analysis)
    
    # Calculate workspace health score
    health_score = await _calculate_workspace_health(analysis)
    
    return WorkspaceAnalysisOutput(
        analysis_summary=analysis["summary"],
        file_patterns=analysis["patterns"],
        automation_suggestions=suggestions,
        integration_opportunities=analysis["integrations"],
        total_files_analyzed=analysis["total_files"],
        workspace_health_score=health_score
    )

async def _perform_workspace_analysis(target_path: Path, depth: str) -> Dict[str, Any]:
    """Perform the actual workspace analysis"""
    
    analysis = {
        "patterns": [],
        "integrations": [],
        "total_files": 0,
        "summary": ""
    }
    
    # Define file patterns to look for
    patterns_config = {
        "data_files": {
            "extensions": [".csv", ".json", ".xlsx", ".xml", ".parquet", ".jsonl"],
            "automation_type": "Data Processing System"
        },
        "api_docs": {
            "patterns": ["*api*", "*swagger*", "*openapi*", "*.postman*"],
            "automation_type": "API Integration System"
        },
        "config_files": {
            "patterns": ["*.config.*", "*.env*", "config.*", "settings.*"],
            "automation_type": "Configuration Management"
        },
        "templates": {
            "extensions": [".template", ".tmpl", ".jinja2"],
            "automation_type": "Template-Based Generation"
        },
        "scripts": {
            "extensions": [".py", ".js", ".sh", ".bat", ".ps1"],
            "automation_type": "Script Automation Enhancement"
        }
    }
    
    pattern_results = {}
    
    # Analyze each pattern type
    for pattern_name, config in patterns_config.items():
        files = []
        total_size = 0
        
        # Search by extensions
        if "extensions" in config:
            for ext in config["extensions"]:
                for file_path in target_path.rglob(f"*{ext}"):
                    if _should_include_file(file_path):
                        files.append(file_path)
                        total_size += file_path.stat().st_size
        
        # Search by patterns
        if "patterns" in config:
            for pattern in config["patterns"]:
                for file_path in target_path.rglob(pattern):
                    if _should_include_file(file_path) and file_path.is_file():
                        files.append(file_path)
                        total_size += file_path.stat().st_size
        
        if files:
            pattern_results[pattern_name] = {
                "files": files,
                "total_size": total_size,
                "automation_type": config["automation_type"]
            }
    
    # Convert to FilePattern objects
    for pattern_name, data in pattern_results.items():
        examples = [str(f.relative_to(target_path)) for f in data["files"][:5]]
        
        analysis["patterns"].append(FilePattern(
            pattern_type=pattern_name.replace("_", " ").title(),
            file_count=len(data["files"]),
            total_size_mb=data["total_size"] / (1024 * 1024),
            examples=examples,
            automation_opportunity=data["automation_type"]
        ))
        
        analysis["total_files"] += len(data["files"])
    
    # Look for integration opportunities
    integration_indicators = {
        "Database": [".sql", "database.py", "db_config", "connection_string"],
        "Cloud Services": ["aws", "azure", "gcp", "s3", "blob"],
        "APIs": ["api_key", "endpoint", "webhook", "rest", "graphql"],
        "Monitoring": ["logging", "metrics", "alerts", "monitoring"],
        "CI/CD": [".github", ".gitlab", "jenkins", "docker", "kubernetes"]
    }
    
    for integration_type, indicators in integration_indicators.items():
        for indicator in indicators:
            # Check in file names and content (basic)
            matches = list(target_path.rglob(f"*{indicator}*"))
            if matches:
                analysis["integrations"].append(f"{integration_type} integration detected")
                break
    
    # Generate summary
    total_patterns = len(analysis["patterns"])
    total_integrations = len(analysis["integrations"])
    
    if total_patterns > 0:
        analysis["summary"] = f"Workspace contains {total_patterns} automation opportunities across {analysis['total_files']} files"
        if total_integrations > 0:
            analysis["summary"] += f" with {total_integrations} integration possibilities"
    else:
        analysis["summary"] = "Workspace appears to be primarily code-based with limited automation file patterns"
    
    return analysis

def _should_include_file(file_path: Path) -> bool:
    """Determine if a file should be included in analysis"""
    
    # Skip hidden directories and common ignore patterns
    ignore_patterns = [
        ".git", "__pycache__", "node_modules", ".pytest_cache", 
        ".venv", "venv", ".env", "dist", "build"
    ]
    
    path_parts = file_path.parts
    for ignore in ignore_patterns:
        if ignore in path_parts:
            return False
    
    # Skip very large files (over 100MB) for performance
    try:
        if file_path.stat().st_size > 100 * 1024 * 1024:
            return False
    except (OSError, IOError):
        return False
    
    return True

async def _generate_automation_suggestions(analysis: Dict[str, Any]) -> List[AutomationSuggestion]:
    """Generate automation suggestions based on workspace analysis"""
    
    suggestions = []
    
    for pattern in analysis["patterns"]:
        if pattern.pattern_type == "Data Files":
            suggestions.append(AutomationSuggestion(
                automation_type="Data Processing Pipeline",
                description=f"Process {pattern.file_count} data files with validation, transformation, and reporting",
                confidence="High" if pattern.file_count > 5 else "Medium",
                estimated_value=f"Save 2-4 hours per processing cycle with {pattern.file_count} files",
                files_involved=pattern.examples
            ))
        
        elif pattern.pattern_type == "Api Docs":
            suggestions.append(AutomationSuggestion(
                automation_type="API Integration System",
                description="Build automated data synchronization with detected APIs",
                confidence="High",
                estimated_value="Enable real-time data sync, reduce manual data entry",
                files_involved=pattern.examples
            ))
        
        elif pattern.pattern_type == "Config Files":
            suggestions.append(AutomationSuggestion(
                automation_type="Configuration Management",
                description="Automate configuration deployment and environment management",
                confidence="Medium",
                estimated_value="Reduce deployment errors, standardize configurations",
                files_involved=pattern.examples
            ))
        
        elif pattern.pattern_type == "Templates":
            suggestions.append(AutomationSuggestion(
                automation_type="Template-Based Generation",
                description="Automate document/report generation using detected templates",
                confidence="High",
                estimated_value="Generate reports automatically, ensure consistency",
                files_involved=pattern.examples
            ))
        
        elif pattern.pattern_type == "Scripts" and pattern.file_count > 10:
            suggestions.append(AutomationSuggestion(
                automation_type="Script Orchestration",
                description="Create workflow automation to orchestrate multiple scripts",
                confidence="Medium",
                estimated_value="Reduce manual script execution, improve reliability",
                files_involved=pattern.examples[:3]  # Just show a few examples
            ))
    
    return suggestions

async def _calculate_workspace_health(analysis: Dict[str, Any]) -> str:
    """Calculate workspace organization health score"""
    
    score_factors = {
        "file_diversity": len(analysis["patterns"]) * 10,  # More file types = better
        "integration_readiness": len(analysis["integrations"]) * 15,  # More integrations = better
        "automation_potential": min(100, analysis["total_files"] * 2)  # More files = more potential
    }
    
    total_score = sum(score_factors.values())
    
    if total_score >= 100:
        return "Excellent (High automation potential with good file organization)"
    elif total_score >= 70:
        return "Good (Multiple automation opportunities identified)"
    elif total_score >= 40:
        return "Fair (Some automation potential, could benefit from better organization)"
    else:
        return "Basic (Limited automation opportunities detected)"
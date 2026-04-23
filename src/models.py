
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

class CVE(BaseModel):
    """Represents a single Common Vulnerability and Exposure (CVE) record."""
    cve_id: str = Field(
        description="The official CVE identifier (e.g., CVE-2023-20198). If no CVE ID is found, write 'Unknown'."
    )
    cvss_score: float = Field(
        description="The CVSS severity score from 1.0 to 10.0. If not found, return 0.0."
    )
    severity: Literal["Low", "Medium", "High", "Critical", "Unknown"] = Field(
        description="The severity level of the vulnerability."
    )
    summary: str = Field(
        description="A brief, 1-2 sentence technical summary of the vulnerability."
    )

class VulnerabilityReport(BaseModel):
    """The final structured report containing all vulnerabilities and lifecycle data for a network device."""

    device_make: str = Field(
        description="The manufacturer of the device (e.g., Cisco, Juniper)."
    )
    device_model: str = Field(
        description="The specific hardware model (e.g., Catalyst 9300, EX4300)."
    )
    os_version: str = Field(
        description="The operating system version running on the device."
    )
    is_end_of_life: bool = Field(
        description="True if the vendor has announced End of Life (EoL) or End of Support for this hardware/OS. False otherwise."
    )
    eol_date: Optional[str] = Field(
        default=None,
        description="The official End of Life date if applicable (YYYY-MM-DD). Return null if not EoL."
    )
    cves: List[CVE] = Field(
        description="A list of the top 3 most critical vulnerabilities affecting this specific OS version.",
        default_factory=list
    )
    recommended_action: str = Field(
        description="A 1-sentence recommendation for the network engineer (e.g., 'Upgrade to IOS-XE 17.6.5')."
    )

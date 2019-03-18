$executable = "%HiSPARC_ROOT%\persistent\startstopbatch\CheckStatus.bat"
$action = New-ScheduledTaskAction -execute $executable
$trigger =  New-ScheduledTaskTrigger -Daily -At 3:00
$taskname = "HiSPARCStatus"
$description = "Reboot computer if one or more HiSPARC processes/services are not running"
$principal = New-ScheduledTaskPrincipal -UserID $(whoami) -LogonType S4U -RunLevel Highest
$dt = ([DateTime]::Now)
$duration = $dt.AddYears(25) -$dt
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit $duration
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $taskname -description $description -Setting $settings  -Principal $principal
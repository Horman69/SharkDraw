# PowerShell script to create a desktop shortcut for SharkDraw with custom icon

$WScriptShell = New-Object -ComObject WScript.Shell

# Path to desktop
$Desktop = [System.Environment]::GetFolderPath('Desktop')

# Create shortcut
$Shortcut = $WScriptShell.CreateShortcut("$Desktop\SharkDraw.lnk")

# Get current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set shortcut properties
$Shortcut.TargetPath = Join-Path $ScriptDir "SharkDraw.vbs"
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.IconLocation = Join-Path $ScriptDir "assets\Logo.ico"
$Shortcut.Description = "SharkDraw - Professional Drawing Application"

# Save the shortcut
$Shortcut.Save()

Write-Host "Ярлык SharkDraw создан на рабочем столе!" -ForegroundColor Green
Write-Host "Теперь вы можете запускать приложение с красивой иконкой!" -ForegroundColor Cyan

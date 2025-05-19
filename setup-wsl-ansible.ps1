# Installs or updates WSL (with Ubuntu) and Ansible for use with Vagrant and VSCode

# Enable WSL and Virtual Machine Platform features
Write-Host "Enabling WSL and Virtual Machine Platform features..."
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart | Out-Null
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart | Out-Null

# Check WSL version
$wslVersion = wsl --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "WSL is installed."
} else {
    Write-Host "Installing WSL..."
    wsl --install
    Write-Host "Please restart your computer and re-run this script."
    exit
}

# Check if Ubuntu is installed
$ubuntuList = wsl -l -q | ForEach-Object { $_.Trim().ToLower() }
$ubuntuInstalled = $false
foreach ($distro in $ubuntuList) {
    if ($distro -eq "ubuntu" -or $distro -like "ubuntu-*") {
        $ubuntuInstalled = $true
        break
    }
}
if (-not $ubuntuInstalled) {
    Write-Host "Installing Ubuntu..."
    wsl --install -d Ubuntu
    Write-Host "Please complete Ubuntu setup in the new window, then re-run this script."
    exit
} else {
    Write-Host "Ubuntu is already installed. Updating Ubuntu..."
    wsl -d Ubuntu -- bash -c "sudo apt-get update && sudo apt-get upgrade -y"
    Write-Host "Checking for Ubuntu release upgrade..."
    # Perform release upgrade if available (non-interactive)
    wsl -d Ubuntu -- bash -c "sudo apt-get install -y update-manager-core"
    $releaseUpgradable = wsl -d Ubuntu -- bash -c "sudo do-release-upgrade -c | grep 'New release'"
    if ($releaseUpgradable) {
        Write-Host "Release upgrade available. Performing release upgrade (this may take a while)..."
        wsl -d Ubuntu -- bash -c "sudo do-release-upgrade -f DistUpgradeViewNonInteractive -y"
    } else {
        Write-Host "No Ubuntu release upgrade available."
    }
}

# Check if Ansible is installed in Ubuntu
$ansibleCheck = wsl -d Ubuntu -- bash -c "dpkg -l | grep ansible"
if ($ansibleCheck) {
    Write-Host "Ansible is already installed. Updating Ansible..."
    wsl -d Ubuntu -- bash -c "sudo apt-get update && sudo apt-get install --only-upgrade -y ansible"
} else {
    Write-Host "Installing Ansible in Ubuntu..."
    wsl -d Ubuntu -- bash -c "sudo apt-get update && sudo apt-get install -y ansible"
}

Write-Host "Ansible is ready in Ubuntu WSL."

# Optional: Install or update VSCode WSL extension (if code CLI is available)
if (Get-Command code -ErrorAction SilentlyContinue) {
    $extList = code --list-extensions
    if ($extList -contains "ms-vscode-remote.remote-wsl") {
        Write-Host "VSCode WSL extension already installed. Updating..."
        code --install-extension ms-vscode-remote.remote-wsl --force
    } else {
        Write-Host "Installing VSCode WSL extension..."
        code --install-extension ms-vscode-remote.remote-wsl
    }
}

Write-Host "Setup complete. You can now use Ansible with Vagrant and VSCode via WSL."

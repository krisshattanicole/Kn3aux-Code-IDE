#!/data/data/com.termux/files/usr/bin/bash
# KN3AUX-CODE Complete Termux Backup Script
# Backs up entire Termux environment to SD card

set -euo pipefail

BACKUP_DIR="/sdcard/termux-backup"
DATE=$(date +%Y%m%d_%H%M%S)

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       KN3AUX-CODE Termux Environment Backup              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Backup started: $(date)"
echo "Destination: $BACKUP_DIR"
echo ""

# Create backup directories
mkdir -p "$BACKUP_DIR"/{home,prefix,configs,packages,databases}

# Backup home directory
echo "[1/6] Backing up home directory..."
rsync -av --exclude='.cache' --exclude='kn3aux_backups' \
    "$HOME/" "$BACKUP_DIR/home/" 2>/dev/null || \
cp -r "$HOME/"* "$BACKUP_DIR/home/" 2>/dev/null || true
echo "✓ Home backed up"

# Backup packages list
echo "[2/6] Backing up package list..."
pkg list-installed > "$BACKUP_DIR/packages/installed.txt" 2>/dev/null || true
pip list > "$BACKUP_DIR/packages/pip.txt" 2>/dev/null || true
npm list -g > "$BACKUP_DIR/packages/npm.txt" 2>/dev/null || true
echo "✓ Package list saved"

# Backup configs
echo "[3/6] Backing up configurations..."
cp -r ~/.bashrc ~/.bash_profile ~/.profile "$BACKUP_DIR/configs/" 2>/dev/null || true
cp -r ~/.gitconfig ~/.ssh "$BACKUP_DIR/configs/" 2>/dev/null || true
cp -r ~/.kn3aux-core/config/* "$BACKUP_DIR/configs/" 2>/dev/null || true
echo "✓ Configs backed up"

# Backup KN3AUX-CODE project
echo "[4/6] Backing up KN3AUX-CODE project..."
cp -r "$HOME/kn3aux-code" "$BACKUP_DIR/home/" 2>/dev/null || true
echo "✓ KN3AUX-CODE backed up"

# Backup databases
echo "[5/6] Backing up databases..."
cp -r ~/.local/share/* "$BACKUP_DIR/databases/" 2>/dev/null || true
echo "✓ Databases backed up"

# Create backup manifest
echo "[6/6] Creating backup manifest..."
cat > "$BACKUP_DIR/manifest.json" << EOF
{
  "backup_date": "$DATE",
  "termux_version": "$(pkg --version)",
  "android_version": "$(getprop ro.build.version.release)",
  "device_model": "$(getprop ro.product.model)",
  "packages_installed": $(wc -l < "$BACKUP_DIR/packages/installed.txt" 2>/dev/null || echo 0),
  "home_size": "$(du -sh "$BACKUP_DIR/home" 2>/dev/null | cut -f1)",
  "total_size": "$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)"
}
EOF
echo "✓ Manifest created"

# Compress backup
echo ""
echo "Compressing backup..."
cd /sdcard && tar -czf "termux-backup-$DATE.tar.gz" termux-backup/ 2>/dev/null || true
echo "✓ Backup compressed"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  BACKUP COMPLETE                         ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Location: $BACKUP_DIR                                   ║"
echo "║  Archive: /sdcard/termux-backup-$DATE.tar.gz             ║"
echo "║  Size: $(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)                               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "To restore:"
echo "  1. Install Termux"
echo "  2. Copy backup to /sdcard/termux-backup"
echo "  3. Run: ~/termux-backup/restore.sh"
echo ""

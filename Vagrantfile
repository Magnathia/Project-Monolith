# Root Vagrantfile to manage multiple Rocky 9 variations in subdirectories

CACHE_DIR = File.expand_path("cache", __dir__)

VAGRANTFILES = [
  "VM/rocky9-cli/Vagrantfile",
  "VM/rocky9-tomcat/Vagrantfile",
  "VM/rocky9-gui/Vagrantfile",
  "VM/rocky9-pxe/Vagrantfile",
  "VM/rocky9-monitor/Vagrantfile"
]

VAGRANTFILES.each do |vf|
  ENV['ROCKY_CACHE_DIR'] = CACHE_DIR
  load File.expand_path(vf, __dir__)
end

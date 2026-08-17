package cloudoptima.terraform

deny contains msg if {
    some resource in input.resource_changes
    resource.type == "aws_instance"
    resource.change.after.associate_public_ip_address == true
    msg := sprintf("EC2 instance %q must not have a public IPv4 address", [resource.name])
}

deny contains msg if {
    some resource in input.resource_changes
    resource.type == "aws_instance"
    resource.change.after.monitoring != true
    msg := sprintf("EC2 instance %q must have detailed monitoring enabled", [resource.name])
}

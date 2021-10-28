variable "key_pair_name" {
  description = "The EC2 Key Pair for SSH access."
  type = string
  default = "klarna-key"
}
variable "docker_registry" {
  description = "The registry should contain the `klarna-solution` image"
  type = string
  default="${DOCKER_REGISTRY}"
}
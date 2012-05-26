$Id$

; API

api = 2

; Core

core = 7.x


; Drupal project.
projects[drupal] = 7.14

; We point to our own installation profile here.
; This profile is the one that we actually are going to use.
projects[feedthebeast][type] = profile
projects[feedthebeast][download][type] = git
projects[feedthebeast][download][url] = git@github.com:lslinnet/profile-feedthebeast.git
projects[feedthebeast][download][branch] = master

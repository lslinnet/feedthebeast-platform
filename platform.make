$Id$

; API

api = 2

; Core

core = 7.x


; Drupal project.
projects[drupal] = 7.14

; We point to our own installation profile here.
; This profile is the one that we actually are going to use.
projects[no_enterprise][type] = profile
projects[no_enterprise][download][type] = git
projects[no_enterprise][download][url] = git@github.com:lslinnet/profile-feedthebeast.git
projects[no_enterprise][download][branch] = master

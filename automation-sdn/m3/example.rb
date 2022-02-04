class webserver::apache {

  $apache = $operatingsystem ? {
    centos => 'httpd',
    ubuntu => 'apache2',
  }

  package { $apache:
    ensure => 'installed',
  }

  service { "$apache":
    enable => true,
    ensure => running,
  }

}

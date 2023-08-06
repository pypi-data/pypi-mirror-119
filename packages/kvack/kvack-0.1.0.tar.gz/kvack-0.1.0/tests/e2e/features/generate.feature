Feature: Generate config files
  Scenario: Black configuration file is generated
    Given there is a config file with black config
    When I run 'kvack gen' in shell
    Then Black configuration file should be generated

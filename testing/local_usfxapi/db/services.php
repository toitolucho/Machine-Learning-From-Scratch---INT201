<?php
$functions = array(
    'local_usfxapi_create_url' => array(
        'classname'   => 'local_usfxapi_external',
        'methodname'  => 'create_url',
        'classpath'   => 'local/usfxapi/externallib.php',
        'description' => 'Creates a URL resource module.',
        'type'        => 'write',
        'ajax'        => true,
    ),
    'local_usfxapi_create_assign' => array(
        'classname'   => 'local_usfxapi_external',
        'methodname'  => 'create_assign',
        'classpath'   => 'local/usfxapi/externallib.php',
        'description' => 'Creates an Assignment module.',
        'type'        => 'write',
        'ajax'        => true,
    )
);

$services = array(
    'USFX API Service' => array(
        'functions' => array('local_usfxapi_create_url', 'local_usfxapi_create_assign'),
        'restrictedusers' => 0,
        'enabled' => 1,
        'shortname' => 'usfxapiservice'
    )
);

<?php
require_once("$CFG->libdir/externallib.php");
require_once("$CFG->dirroot/course/modlib.php");

class local_usfxapi_external extends external_api {
    public static function create_url_parameters() {
        return new external_function_parameters(array(
            'courseid' => new external_value(PARAM_INT, 'Course ID'),
            'sectionnum' => new external_value(PARAM_INT, 'Section number (0, 1, 2...)'),
            'name' => new external_value(PARAM_TEXT, 'Module name'),
            'externalurl' => new external_value(PARAM_URL, 'External URL'),
            'description' => new external_value(PARAM_RAW, 'Description', VALUE_DEFAULT, '')
        ));
    }

    public static function create_url($courseid, $sectionnum, $name, $externalurl, $description = '') {
        global $DB, $USER;
        $params = self::validate_parameters(self::create_url_parameters(), array(
            'courseid' => $courseid,
            'sectionnum' => $sectionnum,
            'name' => $name,
            'externalurl' => $externalurl,
            'description' => $description
        ));
        
        $course = $DB->get_record('course', array('id' => $params['courseid']), '*', MUST_EXIST);
        $context = context_course::instance($course->id);
        self::validate_context($context);
        require_capability('moodle/course:manageactivities', $context);

        $module = new stdClass();
        $module->course = $course->id;
        $module->section = $params['sectionnum'];
        $module->module = $DB->get_field('modules', 'id', array('name' => 'url'));
        $module->modulename = 'url';
        $module->name = $params['name'];
        $module->externalurl = $params['externalurl'];
        $module->introeditor = array('text' => $params['description'], 'format' => FORMAT_HTML);
        $module->visible = 1;

        $modinfo = add_moduleinfo($module, $course);
        return $modinfo->coursemodule;
    }

    public static function create_url_returns() {
        return new external_value(PARAM_INT, 'Course Module ID');
    }

    public static function create_assign_parameters() {
        return new external_function_parameters(array(
            'courseid' => new external_value(PARAM_INT, 'Course ID'),
            'sectionnum' => new external_value(PARAM_INT, 'Section number (0, 1, 2...)'),
            'name' => new external_value(PARAM_TEXT, 'Assignment name'),
            'description' => new external_value(PARAM_RAW, 'Description', VALUE_DEFAULT, '')
        ));
    }

    public static function create_assign($courseid, $sectionnum, $name, $description = '') {
        global $DB, $USER;
        $params = self::validate_parameters(self::create_assign_parameters(), array(
            'courseid' => $courseid,
            'sectionnum' => $sectionnum,
            'name' => $name,
            'description' => $description
        ));

        $course = $DB->get_record('course', array('id' => $params['courseid']), '*', MUST_EXIST);
        $context = context_course::instance($course->id);
        self::validate_context($context);
        require_capability('moodle/course:manageactivities', $context);

        $module = new stdClass();
        $module->course = $course->id;
        $module->section = $params['sectionnum'];
        $module->module = $DB->get_field('modules', 'id', array('name' => 'assign'));
        $module->modulename = 'assign';
        $module->name = $params['name'];
        $module->introeditor = array('text' => $params['description'], 'format' => FORMAT_HTML);
        $module->alwaysshowdescription = 1;
        $module->submissiondrafts = 0;
        $module->assignsubmission_file_enabled = 1;
        $module->assignsubmission_file_maxfiles = 1;
        $module->assignsubmission_file_maxsizebytes = 0;
        $module->visible = 1;

        $modinfo = add_moduleinfo($module, $course);
        return $modinfo->coursemodule;
    }

    public static function create_assign_returns() {
        return new external_value(PARAM_INT, 'Course Module ID');
    }
}

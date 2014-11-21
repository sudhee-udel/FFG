<?php defined('BASEPATH') OR exit('No direct script access allowed');
/**
 * BAGCA Events Class
 * 
 * @package        PyroCMS
 * @subpackage    BAGCA Module
 * @category    events
 * @author        Jerel Unruh - PyroCMS Dev Team
 * @website        http://unruhdesigns.com
 */
class Events_BAGCA {
    
    protected $ci;
    
    public function __construct()
    {
        $this->ci =& get_instance();
        
        //register the public_controller event
        Events::register('public_controller', array($this, 'run'));
		
		//register a second event that can be called any time.
		// To execute the "run" method below you would use: Events::trigger('bagca_event');
		// in any php file within PyroCMS, even another module.
		Events::register('bagca_event', array($this, 'run'));
    }
    
    public function run()
    {
        $this->ci->load->model('bagca/bagca_m');
        
        // we're fetching this data on each front-end load. You'd probably want to do something with it IRL
        $this->ci->bagca_m->limit(5)->get_all();
    }
    
}
/* End of file events.php */

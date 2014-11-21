<?php if (!defined('BASEPATH')) exit('No direct script access allowed');
/**
 * This is a bagca module for PyroCMS
 *
 * @author 		Jerel Unruh - PyroCMS Dev Team
 * @website		http://unruhdesigns.com
 * @package 	PyroCMS
 * @subpackage 	BAGCA Module
 */
class BAGCA_m extends MY_Model {

	public function __construct()
	{		
		parent::__construct();
		
		/**
		 * If the bagca module's table was named "bagcas"
		 * then MY_Model would find it automatically. Since
		 * I named it "bagca" then we just set the name here.
		 */
		$this->_table = 'bagca';
	}
	
	//create a new item
	public function create($input)
	{
		$to_insert = array(
			'name' => $input['name'],
			'slug' => $this->_check_slug($input['slug'])
		);

		return $this->db->insert('bagca', $to_insert);
	}

	//make sure the slug is valid
	public function _check_slug($slug)
	{
		$slug = strtolower($slug);
		$slug = preg_replace('/\s+/', '-', $slug);

		return $slug;
	}
}

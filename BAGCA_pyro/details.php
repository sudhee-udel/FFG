<?php defined('BASEPATH') or exit('No direct script access allowed');

class Module_Bagca extends Module {

	public $version = '2.1';

	public function info()
	{
		return array(
			'name' => array(
				'en' => 'BAGCA'
			),
			'description' => array(
				'en' => 'This is a PyroCMS module bagca.'
			),
			'frontend' => TRUE,
			'backend' => TRUE,
			'menu' => 'content', // You can also place modules in their top level menu. For example try: 'menu' => 'BAGCA',
			'sections' => array(
				'items' => array(
					'name' 	=> 'bagca:items', // These are translated from your language file
					'uri' 	=> 'admin/bagca',
						'shortcuts' => array(
							'create' => array(
								'name' 	=> 'bagca:create',
								'uri' 	=> 'admin/bagca/create',
								'class' => 'add'
								)
							)
						)
				)
		);
	}

	public function install()
	{
		$this->dbforge->drop_table('bagca');
		$this->db->delete('settings', array('module' => 'bagca'));

		$bagca = array(
                        'id' => array(
									  'type' => 'INT',
									  'constraint' => '11',
									  'auto_increment' => TRUE
									  ),
						'name' => array(
										'type' => 'VARCHAR',
										'constraint' => '100'
										),
						'slug' => array(
										'type' => 'VARCHAR',
										'constraint' => '100'
										)
						);

		$bagca_setting = array(
			'slug' => 'bagca_setting',
			'title' => 'BAGCA Setting',
			'description' => 'A Yes or No option for the BAGCA module',
			'`default`' => '1',
			'`value`' => '1',
			'type' => 'select',
			'`options`' => '1=Yes|0=No',
			'is_required' => 1,
			'is_gui' => 1,
			'module' => 'bagca'
		);

		$this->dbforge->add_field($bagca);
		$this->dbforge->add_key('id', TRUE);

		if($this->dbforge->create_table('bagca') AND
		   $this->db->insert('settings', $bagca_setting) AND
		   is_dir($this->upload_path.'bagca') OR @mkdir($this->upload_path.'bagca',0777,TRUE))
		{
			return TRUE;
		}
	}

	public function uninstall()
	{
		$this->dbforge->drop_table('bagca');
		$this->db->delete('settings', array('module' => 'bagca'));
		{
			return TRUE;
		}
	}


	public function upgrade($old_version)
	{
		// Your Upgrade Logic
		return TRUE;
	}

	public function help()
	{
		// Return a string containing help info
		// You could include a file and return it here.
		return "No documentation has been added for this module.<br />Contact the module developer for assistance.";
	}
}
/* End of file details.php */

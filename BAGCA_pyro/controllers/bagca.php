<?php if (!defined('BASEPATH')) exit('No direct script access allowed');
/**
 * This is a bagca module for PyroCMS
 *
 * @author 		Jerel Unruh - PyroCMS Dev Team
 * @website		http://unruhdesigns.com
 * @package 	PyroCMS
 * @subpackage 	BAGCA Module
 */
class BAGCA extends Public_Controller
{
	public function __construct()
	{
		parent::__construct();

		// Load the required classes
		$this->load->model('bagca_m');
		$this->lang->load('bagca');
        $this->load->helper('form');
        $this->load->library('Session');

		$this->template
			->append_css('module::bagca.css')
			->append_js('module::bagca.js');
	}

	/**
	 * All items
	 */
	public function index($offset = 0)
	{
		// set the pagination limit
		$limit = 5;
		
		$items = $this->bagca_m->limit($limit)
			->offset($offset)
			->get_all();
			
		// we'll do a quick check here so we can tell tags whether there is data or not
		$items_exist = count($items) > 0;

		// we're using the pagination helper to do the pagination for us. Params are: (module/method, total count, limit, uri segment)
		$pagination = create_pagination('bagca', $this->bagca_m->count_all(), $limit, 2);

		$this->template
			->title($this->module_details['name'], 'the rest of the page title')
			/*->set('items', $items)
			->set('items_exist', $items_exist)
			->set('pagination', $pagination)*/
			->build('index');
	}

    public function evaluate()
    {
        //echo $_GET["question_1"];
        //echo $_GET["question_2"];

        if($_GET["question_1"] == "Delaware" && $_GET["question_2"] == "America")
        {
            $this->session->set_flashdata("success", "You have passed the quiz!");
        }else
        {
            $this->session->set_flashdata("error", "You have failed the quiz! Please try again.");
        }

        redirect('BAGCA/index');
    }
}

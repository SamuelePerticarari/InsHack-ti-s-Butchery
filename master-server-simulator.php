<?php

if( !isset($_POST['flag']) )
{


	function generate_string($strength = 31) {
			$permitted_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
	    $permitted_chars_length = strlen($permitted_chars);
	    $random_string = '';
	    for($i = 0; $i < $strength; $i++) {
	        $random_character = $permitted_chars[mt_rand(0, $permitted_chars_length - 1)];
	        $random_string .= $random_character;
	    }

	    return $random_string . '=';
	}

	echo generate_string();

}else{
		// Sleep 700 ms
		usleep( 100 * 1000 );

		$n = rand(1, 10);

		switch($n)
		{
			case 1:
			case 7:
				$arr = [
					'status' => 'error',
					'message' => 'The submitted flag is expired.'
				];
				echo json_encode($arr);
				break;

			case 2:
			case 4:
			case 5:
			case 6:
			case 8:
			case 9:
			case 10:
				$arr = [
					'status' => 'success',
					'message' => 'Flag accepted!'
				];
				echo json_encode($arr);
				break;


			case 3:
				$arr = [
					'status' => 'success',
					'message' => 'You submitted a duplicated flag!'
				];
				echo json_encode($arr);
		  	break;
		}
}

?>

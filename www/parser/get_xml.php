<?php

	function getFile($file){

		$curl = curl_init();
		curl_setopt($curl, CURLOPT_URL, (preg_match('%http%', $file) ? $file : 'http://assets.transistor.ru/catalog/transistor_catalog.xml.gz?category='.$file));
		curl_setopt($curl, CURLOPT_POST, 1);
		curl_setopt($curl, CURLOPT_POSTFIELDS, array('greeting' => 'hi!'));
		curl_setopt($curl, CURLOPT_USERPWD, 'roman.hohlov@mail.ru:28456hrvn'); 
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		$result = curl_exec($curl);
		curl_close($curl);

		$gz_filename = 'xml/transistor_catalog_'.$file.'.xml.gz';
		if(!$handle = fopen($gz_filename, 'w'))
			echo 'не могу открыть файл для записи на сервере';

		if(!fwrite($handle, $result))
			echo 'не могу записать в файл данные';
		fclose($handle);

		if (filesize($gz_filename) > 3072){
			// Распаковать zip
			$gzhandle = gzopen($gz_filename, 'r');
			$handle = fopen(substr($gz_filename, 0, -3), 'w');
			while (!feof($gzhandle))
			{
				$buf = gzread($gzhandle, 8192);
				fwrite($handle, $buf);
			}

			gzclose($gzhandle);
			fclose($handle);
			
			// Удалить zip
			unlink('xml/transistor_catalog_'.$file.'.xml.gz');
			
			print '<h3>Cкачан файл transistor_catalog_'.$file.'.xml</h3>';
		}
		else {
			unlink('xml/transistor_catalog_'.$file.'.xml.gz');
			print '<h3 style="color:red">Прайс transistor_catalog_'.$file.'.xml не обновлен</h3>';
			//exit;
		}
	}

?>
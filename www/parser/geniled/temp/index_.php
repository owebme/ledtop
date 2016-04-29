<?php
  function getXLS($xls){
    include_once 'Classes/PHPExcel/IOFactory.php';
    $objPHPExcel = PHPExcel_IOFactory::load($xls);
    $objPHPExcel->setActiveSheetIndex(0);
    $aSheet = $objPHPExcel->getActiveSheet();
 
    //���� ������ ����� ��������� ������� ���������� � ���� �������� ����� ������ ������
    $array = array();
    //������� �������� ������ � ��������� �� ���� ������
    foreach($aSheet->getRowIterator() as $row){
      //������� �������� ����� ������� ������
      $cellIterator = $row->getCellIterator();
      //��������� ������ �� ������� ������
      //���� ������ ����� ��������� �������� ������ ��������� ������
      $item = array();
      foreach($cellIterator as $cell){
        //������� �������� ����� ����� ������ � ��������� ������
        array_push($item, iconv('utf-8', 'cp1251', $cell->getCalculatedValue()));
      }
      //������� ������ �� ���������� ����� ��������� ������ � "����� ����� �����"
      array_push($array, $item);
    }
    return $array;
  }
 
  $xlsData = getXLS('price.xlsx'); //�������� ������ �� XLS
?>
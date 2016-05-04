CREATE TABLE IF NOT EXISTS `catalog_providers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `color` varchar(24) NOT NULL,
  `alias` varchar(24) NOT NULL,
  `date` datetime NOT NULL,  
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=cp1251;

INSERT INTO `catalog_providers` VALUES
(1, 'Alright', 'red', 'alright', '2016-04-27 02:16:42'),
(2, 'Geniled', 'green', 'geniled', '2016-04-27 02:18:42');

CREATE TABLE IF NOT EXISTS `cat_category_links` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `p_cid` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,  
  `bind` tinyint(1) NOT NULL DEFAULT '1',
  KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=cp1251;

alter table cat_category_links add index (p_id);
alter table cat_category_links add index (p_cid);

alter table catalog_alright add index (c_pid);

alter table cat_category add index (c_pid);

alter table cat_product add primary key (p_id);
alter table cat_product add unique (p_art);
alter table cat_product add index (p_name);
alter table cat_product add index (cat_id);

alter table cat_product_rel add index (cat_p_id);
alter table cat_product_rel add index (cat_id);
alter table cat_product_rel add index (p_pos);
alter table cat_product_rel add unique p_id__c_id__main(cat_p_id, cat_id, cat_main);

alter table cat_product_fields add index (p_id);

alter table cat_product_filters add index (gid);
alter table cat_product_filters add index (f_pid);
alter table cat_product_filters add index gid__f_pid(gid, f_pid);
alter table cat_product_filters add index f_pid__name(f_pid, name);

alter table cat_product_hits add index (hit_id);

alter table cat_orders add index (status);
alter table cat_orders add index ch_region__status(ch_region, status);

alter table cat_orders_product add index (order_id);

alter table users_data add primary key (user_id);

alter table users_group_category add index (group_id);
alter table users_group_category add index group_id__cat_id(group_id, cat_id);

alter table goals add index date__ip(date_goal, ip);

EXPLAIN SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='21'  AND p.p_show != '0'

EXPLAIN SELECT p.* FROM cat_category AS cat JOIN cat_category_links AS link ON(cat.c_id=link.id) JOIN products_alright AS p ON(link.p_cid = p.cat_id) WHERE cat.c_id ='89'

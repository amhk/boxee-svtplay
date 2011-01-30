import mc

import svtplay

def Play(url):
	player = mc.GetPlayer()
	item = mc.ListItem()
	item.SetPath(url)
	player.Play(item)

def SetListItems(new_items):
	list = mc.GetActiveWindow().GetList($(list/main))
	itemList = mc.ListItems()

	for i in new_items:
		item = mc.ListItem()
		item.SetLabel(i.title)
		item.SetPath(i.url)
		item.SetDescription(i.description)
		item.SetThumbnail(i.thumbnail)

		itemList.append(item)

	list.SetItems(itemList)

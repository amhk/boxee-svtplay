import mc

import svtplay

def Play(url):
	player = mc.GetPlayer()
	item = mc.ListItem()
	item.SetPath(url)
	player.Play(item)

def SetListItems(new_items): # FIXME: add parameter: list id
	list = mc.GetActiveWindow().GetList($(list/main))
	itemList = mc.ListItems()

	for i in new_items:
		item = mc.ListItem()
		item.SetLabel(i['title'])
		item.SetThumbnail(i['thumbnail'])
		#item.SetPath(i.url)
		#item.SetDescription(i.description)

		itemList.append(item)

	list.SetItems(itemList)

#def ActivateWindow(src, dest):
#list = mc.GetActiveWindow().GetList($(list/main))
#index = list.GetFocusedItem()
#params = mc.Parameters()
#params['back'] = '$(window/main)'
#params['path'] = str(index)
#mc.GetApp().ActivateWindow($(window/title), params)

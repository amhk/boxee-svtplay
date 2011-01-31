import mc

import svtplay

ID_LIST_MAIN = $(list/main)
ID_LIST_TITLE = $(list/title)
ID_WINDOW_TITLE = $(window/title)

def Play(url):
	player = mc.GetPlayer()
	item = mc.ListItem()
	item.SetPath(url)
	player.Play(item)

def SetListItems(list_id, new_items):
	list = mc.GetActiveWindow().GetList(list_id)
	itemList = mc.ListItems()

	for i in new_items:
		item = mc.ListItem()
		item.SetLabel(i['title'])
		item.SetThumbnail(i['thumbnail'])
		#item.SetPath(i.url)
		#item.SetDescription(i.description)

		itemList.append(item)

	list.SetItems(itemList)

def ActivateWindow(win_id):
	params = mc.Parameters()
	params["title"] = "FIXME:title"
	mc.GetApp().ActivateWindow(win_id, params)

#def ActivateWindow(src, dest):
#list = mc.GetActiveWindow().GetList($(list/main))
#index = list.GetFocusedItem()
#params = mc.Parameters()
#params['back'] = '$(window/main)'
#params['path'] = str(index)
#mc.GetApp().ActivateWindow($(window/title), params)

import hou

desktop = hou.ui.curDesktop()   ## Desktop Class
panel_float_tab = desktop.createFloatingPanel(hou.paneTabType.NetworkEditor)   # floatingPanel Class
panel_float_tab.setName("USD_IMPORTER")

panel_float_tab.panes()[0].splitVertically()    #Pane

panel_float_tab.panes()[0].showPaneTabsStow(False) 
panel_float_tab.panes()[1].showPaneTabsStow(False) 

pp1 = panel_float_tab.paneTabs()[0].setType(hou.paneTabType.PythonPanel)
pp1.showToolbar(False) 

pp2 = panel_float_tab.paneTabs()[1].setType(hou.paneTabType.PythonPanel)

pp1.setActiveInterface(hou.pypanel.interfaceByName("MS_USD_Converter"))
pp2.setActiveInterface(hou.pypanel.interfaceByName("layout_asset_gallery"))

lag = pp2.activeInterface()



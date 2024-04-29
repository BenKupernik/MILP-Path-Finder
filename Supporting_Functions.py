# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:18:06 2024

@author: benk
"""

TOP = 0
RIGHT = 1
BOT = 2
LEFT = 3



class cell():
    def __init__ (self, cell_id, x_center, y_center, grid, start_or_end_cell):
        self.top_right_vert = None
        self.bot_right_vert = None
        self.bot_left_vert = None
        self.top_left_vert = None
        self.num_cell_edges = 4
        self.start_or_end_cell = start_or_end_cell
        self.edges = {}
        self.distance_coefs = {}
        self.cell_row = cell_id[0]
        self.cell_column = cell_id[1]
        self.cell_id = str(self.cell_row) + '_' + str(self.cell_column)
        
        
        # use the grid to get the vertices for this cell
        self.get_verts(grid)
        # now make some edges with them. 
        # edges will be stored as a dict in the form {cell_id_top: (top_left_vert, top_right_vert)..... }
        self.get_edges()
        # now get the distance coeficents. Will be stored in the same structure as the edges
        self.get_distance_coefs(x_center, y_center)
        
    def get_verts(self, grid):
        # find the verts with the grid function
        vert_list = grid.get_cell_vertices(self.cell_row, self.cell_column)
        assert len(vert_list) == 4, '%s vertices were found on cell %s. There should be 4' % (len(vert_list), self.cell_id)
        # figure out which vertex is which
        x_cords = [vert[0] for vert in vert_list]
        y_cords = [vert[1] for vert in vert_list]
        for vert in vert_list:
            if vert[0] == max(x_cords) and vert[1] == max(y_cords):
                self.top_right_vert = vert
            elif vert[0] == max(x_cords) and vert[1] == min(y_cords):
                self.bot_right_vert = vert
            elif vert[0] == min(x_cords) and vert[1] == min(y_cords):
                self.bot_left_vert = vert
            elif vert[0] == min(x_cords) and vert[1] ==  max(y_cords):
                self.top_left_vert = vert
            else:
                raise ValueError('A vertex could not be classified as the corner of a square. \n Are the cells squares?')
    def get_edges(self):
        # group the vertices into edges and lable what side there on. 
        cell_id_string = str(self.cell_row) + '_' + str(self.cell_column) + '_'
        self.edges[cell_id_string + 'top'] = [self.top_left_vert, self.top_right_vert]
        self.edges[cell_id_string + 'right'] = [self.top_right_vert, self.bot_right_vert]
        self.edges[cell_id_string + 'bot'] = [self.bot_right_vert, self.bot_left_vert]
        self.edges[cell_id_string + 'left'] = [self.bot_left_vert, self.top_left_vert]
    
    def get_vers_by_edge(self, edge_name):
        # check id's match 0_7_bot
        row, col, edge = edge_name.split('_')
        if int(row) == int(self.cell_row) and int(col) == int(self.cell_column):
            return self.edges.get(edge_name)
        else:
            return None
        
        
    def get_distance_coefs(self, x_center, y_center):
        self.distance_coefs['top'] = self.top_right_vert[1] - y_center
        self.distance_coefs['right'] = self.top_right_vert[0] - x_center
        self.distance_coefs['bot'] =  y_center - self.bot_left_vert[1]
        self.distance_coefs['left'] =  x_center - self.bot_left_vert[0]
        
        
def move_cell_id(cell_id, direction_x=None, direction_y=None):
    row, col = cell_id.split('_')
    if direction_x is not None:
        if direction_x == 'left':
            col = int(col) - 1
        elif direction_x == 'right':
            col = int(col) + 1
        else:
            raise(AttributeError, '%s direction not known' % direction_x)

    if direction_y is not None:
        if direction_y == 'up':
            row = int(row) - 1
        elif direction_y == 'down':
            row = int(row) + 1
        else:
            raise(AttributeError, '%s direction not known' % direction_y) 

    return str(row) + '_' + str(col)

def get_opposing_edge(cell_id, edge, neibros, desc_vars):
    # get the oposing cell edge descision varable 
    TOP = 0
    RIGHT = 1
    BOT = 2
    LEFT = 3
    opposing_edge = None
    
    if 'top' in str(edge):
        if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
            opposing_edge = desc_vars.get(new_cell)[BOT]
    elif 'right' in str(edge):
        if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
            opposing_edge = desc_vars.get(new_cell)[LEFT]
    elif 'bot' in str(edge):
        if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
            opposing_edge = desc_vars.get(new_cell)[TOP]
    elif 'left' in str(edge):
        if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
            opposing_edge = desc_vars.get(new_cell)[RIGHT]

    return opposing_edge

def get_neighboring_edges(cell_id, edge, neibros, desc_vars):
    # left and top are input directions, down and right are output directions
    # the desc_var dict stores a list that holdes edges in order top, right, bot, left

    
    input_edges = []
    output_edges = []
    if 'top' in str(edge):
        # check for cell to the left
        if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[TOP])
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
        # upper left cell
        if (new_cell := move_cell_id(cell_id, direction_x = 'left' , direction_y = 'up')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
            input_edges.append(desc_vars.get(new_cell)[BOT])
        # upper cell
        if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[BOT])
            input_edges.append(desc_vars.get(new_cell)[LEFT])
            
            output_edges.append(desc_vars.get(new_cell)[RIGHT])
            output_edges.append(desc_vars.get(new_cell)[BOT])
        # top right
        if (new_cell := move_cell_id(cell_id, direction_x = 'right', direction_y = 'up')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[BOT])
        # right
        if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[TOP])
            
        # include edges on the cell itself
        input_edges.append(desc_vars.get(cell_id)[LEFT])
        output_edges.append(desc_vars.get(cell_id)[RIGHT]) 
        
    if 'right' in str(edge):
         # check for cell to the top
        if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
            # top, right, bot, left
            input_edges.append(desc_vars.get(new_cell)[BOT])
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
        # check top right cell
        if (new_cell := move_cell_id(cell_id, direction_x = 'right', direction_y = 'up')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[BOT])
            input_edges.append(desc_vars.get(new_cell)[LEFT])
            
        # check right cell
        if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[LEFT])
            input_edges.append(desc_vars.get(new_cell)[TOP])
            
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[BOT])
            
        # check bot right cell
        if (new_cell := move_cell_id(cell_id, direction_x = 'right', direction_y = 'down' )) in neibros:
            output_edges.append(desc_vars.get(new_cell)[TOP])
            output_edges.append(desc_vars.get(new_cell)[LEFT])
        # check bot  cell
        if (new_cell := move_cell_id(cell_id, direction_y = 'down' )) in neibros:
            output_edges.append(desc_vars.get(new_cell)[TOP])
            output_edges.append(desc_vars.get(new_cell)[RIGHT])
            
        # include edges on the cell itself
        input_edges.append(desc_vars.get(cell_id)[TOP])
        output_edges.append(desc_vars.get(cell_id)[BOT]) 
            
    if 'bot' in str(edge):
         # check for cell to the left
        if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
            # top, right, bot, left
            input_edges.append(desc_vars.get(new_cell)[BOT])
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
         # check for cell to the left and down
        if (new_cell := move_cell_id(cell_id, direction_x = 'left', direction_y = 'down')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[TOP])
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
         # down cell
        if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[TOP])
            input_edges.append(desc_vars.get(new_cell)[LEFT])
            
            output_edges.append(desc_vars.get(new_cell)[TOP])
            output_edges.append(desc_vars.get(new_cell)[RIGHT])
            
        # cell down and to the right
        if (new_cell := move_cell_id(cell_id, direction_x = 'right', direction_y = 'down')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[TOP])
         # cell to the right
        if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[BOT])  
        
        # include edges on the cell itself
        input_edges.append(desc_vars.get(cell_id)[LEFT])
        output_edges.append(desc_vars.get(cell_id)[RIGHT]) 
            
            
    if 'left' in str(edge): 
         # check for cell to the top
        if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
            # top, right, bot, left
            input_edges.append(desc_vars.get(new_cell)[LEFT])
            input_edges.append(desc_vars.get(new_cell)[BOT])
         # check for cell to the top left
        if (new_cell := move_cell_id(cell_id, direction_x = 'left', direction_y = 'up')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
            input_edges.append(desc_vars.get(new_cell)[BOT])
         # check for cell to the left
        if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
            input_edges.append(desc_vars.get(new_cell)[RIGHT])
            input_edges.append(desc_vars.get(new_cell)[TOP])
            
            output_edges.append(desc_vars.get(new_cell)[BOT])
            output_edges.append(desc_vars.get(new_cell)[RIGHT])
            
         # cell to the bottom left
        if (new_cell := move_cell_id(cell_id, direction_x = 'left', direction_y = 'down')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[TOP])
            output_edges.append(desc_vars.get(new_cell)[LEFT])     
            
         # cell to the bottom 
        if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
            output_edges.append(desc_vars.get(new_cell)[LEFT])
            output_edges.append(desc_vars.get(new_cell)[TOP]) 
         
        # include edges on the cell itself
        input_edges.append(desc_vars.get(cell_id)[TOP])
        output_edges.append(desc_vars.get(cell_id)[BOT]) 
            
    return input_edges, output_edges        
        
        
def is_neighboring(center_cell, cell):
    adjacent_row = False
    adjacent_col = False
    if center_cell.cell_id != cell.cell_id:
        if abs(center_cell.cell_row - cell.cell_row) <= 1:
            adjacent_row = True
        if abs(center_cell.cell_column - cell.cell_column) <= 1:
            adjacent_col = True
            
    return adjacent_row and adjacent_col       
        

def get_box_combos(cell_id, neibros, desc_vars):
    box_combo_list = []
    
    # get combo where 4 boxes have 1 edge active
    # get each opposing edge 
    edge_list = [get_opposing_edge(cell_id, edge, neibros, desc_vars) for edge in desc_vars.get(cell_id)]
    
    # check for None values
    edge_list = [edge for edge in edge_list if edge is not None]
    # if there are 4 non Nove values in the list
    if len(edge_list) == 4:
        box_combo_list.append(edge_list)    
    
    # handle cases where 3 cells form a box T = top L = left i = inner O = outer ect
    # To + Bo + Li + lo
    edge_list = []
    if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[BOT])
        
    if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[TOP])
        
    # if both a cell above and below exist
    if len(edge_list) == 2:
        edge_list.append(desc_vars.get(cell_id)[LEFT])
        edge_list.append(desc_vars.get(cell_id)[RIGHT])
        # add it to the list of lists to be returned
        box_combo_list.append(edge_list)
    
    
    # reset edge list and check next combo Lo + Ro + Ti + Bi
    edge_list = []
    if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[LEFT])
        
    if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[RIGHT])
        
    # if both a cell above and below exist
    if len(edge_list) == 2:
        edge_list.append(desc_vars.get(cell_id)[TOP])
        edge_list.append(desc_vars.get(cell_id)[BOT])
        # add it to the list of lists to be returned
        box_combo_list.append(edge_list)
               
    
    # same deal now To + Ro + Bi + Li
    edge_list = []
    if (new_cell := move_cell_id(cell_id, direction_y = 'up')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[BOT])
        
    if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[LEFT])
        
    # if both a cell above and below exist
    if len(edge_list) == 2:
        edge_list.append(desc_vars.get(cell_id)[LEFT])
        edge_list.append(desc_vars.get(cell_id)[BOT])
        # add it to the list of lists to be returned
        box_combo_list.append(edge_list)
        
    
    # Ti + Ro + Bo+ Li
    edge_list = []
    if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[TOP])
        
    if (new_cell := move_cell_id(cell_id, direction_x = 'right')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[LEFT])
        
    # if both a cell above and below exist
    if len(edge_list) == 2:
        edge_list.append(desc_vars.get(cell_id)[LEFT])
        edge_list.append(desc_vars.get(cell_id)[TOP])
        # add it to the list of lists to be returned
        box_combo_list.append(edge_list)
        
        
    # Finaly Ti + Ri + Bo + Lo
    edge_list = []
    if (new_cell := move_cell_id(cell_id, direction_y = 'down')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[TOP])
        
    if (new_cell := move_cell_id(cell_id, direction_x = 'left')) in neibros:
        edge_list.append(desc_vars.get(new_cell)[RIGHT])
        
    # if both a cell above and below exist
    if len(edge_list) == 2:
        edge_list.append(desc_vars.get(cell_id)[RIGHT])
        edge_list.append(desc_vars.get(cell_id)[TOP])
        # add it to the list of lists to be returned
        box_combo_list.append(edge_list)
    
        
    return box_combo_list

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
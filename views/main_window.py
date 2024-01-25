# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledNsDmWk.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from logic.dfa import Dfa
from logic.degree import Degree
from logic.regular_language import RegularExpressionAnalyzer


class Ui_MainWindow(object):
    STATES = []
    ALPHABETS = []
    TRANSACTIONS = {}
    START_STATE = ''
    ACCEPT_STATES = []

    STATES_1 = []
    ALPHABETS_1 = []
    TRANSACTIONS_1 = {}
    START_STATE_1 = ''
    ACCEPT_STATES_1 = []

    Expression_1 = ''
    Expression_2 = ''

    def on_btn_add_StateName(self):
        user_input = self.txt_StateName.toPlainText()
        if user_input != "":
            if user_input not in self.STATES:
                if self.cb_finall_state.isChecked() == True:
                    self.ACCEPT_STATES.append(self.txt_StateName.toPlainText())
                self.STATES.append(self.txt_StateName.toPlainText())
                self.listWidget_StatesName.addItem(self.STATES[-1])
                self.update_initial_and_final_state()

    def on_btn_add_Alphabet(self):
        user_input = self.txt_Alphabet.toPlainText()
        if len(user_input) == 1:
            if user_input not in self.ALPHABETS:
                self.ALPHABETS.append(self.txt_Alphabet.toPlainText())
                self.listWidget_Alphabet.addItem(self.ALPHABETS[-1])
    
    def remove_selected_item_listwidget_states(self):
        selected_items = self.listWidget_StatesName.selectedItems()

        for item in selected_items:
            row = self.listWidget_StatesName.row(item)
            self.STATES.remove(item.text())
            if item.text() in self.ACCEPT_STATES:
                self.ACCEPT_STATES.remove(item.text())
            self.listWidget_StatesName.takeItem(row)
            del item
            self.update_initial_and_final_state()

    def remove_selected_item_listwidget_alphabet(self):
        selected_items = self.listWidget_Alphabet.selectedItems()

        for item in selected_items:
            row = self.listWidget_Alphabet.row(item)
            self.ALPHABETS.remove(item.text())
            self.listWidget_Alphabet.takeItem(row)
            del item

    def on_page_Transaction_shown(self, event):
        self.combo_CurrentStates.clear()
        self.combo_Transactions.clear()
        self.combo_TargetStates.clear()

        self.combo_CurrentStates.addItems(self.STATES)
        self.combo_Transactions.addItems(self.ALPHABETS)
        self.combo_TargetStates.addItems(self.STATES)

        self.populate_table()

    def update_initial_and_final_state(self):
        self.combo_InitialState.clear()
        self.combo_InitialState.addItems(self.STATES)

        self.combo_Equivalent_InitialState.clear()
        self.combo_Equivalent_InitialState.addItems(self.STATES_1)

    def on_btn_add_Transaction(self):
        current_state = self.combo_CurrentStates.currentText()
        transaction = self.combo_Transactions.currentText()
        target_state = self.combo_TargetStates.currentText()

        self.TRANSACTIONS[(current_state, transaction)] = target_state
        self.populate_table()


    def populate_table(self):
        self.tableWidget_Transaction.setRowCount(len(self.TRANSACTIONS))
        for row_index, ((current_state, transaction), target_state) in enumerate(self.TRANSACTIONS.items()):
            self.tableWidget_Transaction.setItem(row_index, 0, QTableWidgetItem(current_state))
            self.tableWidget_Transaction.setItem(row_index, 1, QTableWidgetItem(transaction))
            self.tableWidget_Transaction.setItem(row_index, 2, QTableWidgetItem(target_state))


    def on_btn_save(self):
        self.listWidget_AllString.clear()
        self.START_STATE = self.combo_InitialState.currentText()
        dfa = Dfa(
            states=self.STATES,
            alphabet=self.ALPHABETS,
            transitions=self.TRANSACTIONS,
            start_state=self.START_STATE,
            accept_states=self.ACCEPT_STATES
        )
        if dfa.is_empty_language():
            self.lbl_result_is_empty_language.setText("Is Empty")
        else:
            self.lbl_result_is_empty_language.setText("Isn't Empty")

        if dfa.is_finite():
            self.lbl_result_is_finite.setText("Is finite")
        else:
            self.lbl_result_is_finite.setText("Isn't finite")

        all_string = dfa.all_strings()
        if all_string is not None:
            self.lbl_result_allStrings.setText(str(all_string[1]))
            self.listWidget_AllString.addItems(all_string[0])
            if "" in all_string[0]:
                self.listWidget_AllString.addItem("Empty string")
    
    def on_test_string(self):
        dfa = Dfa(
            states=self.STATES,
            alphabet=self.ALPHABETS,
            transitions=self.TRANSACTIONS,
            start_state=self.START_STATE,
            accept_states=self.ACCEPT_STATES
        )
        if dfa.accepts_string(self.textEdit_2.toPlainText()):
            self.lbl_result_test_string.setText("Accepted")
        else:
            self.lbl_result_test_string.setText("Not accepted")
    
    def on_page_Minimize_shown(self, event):
        dfa = Dfa(
            states=self.STATES,
            alphabet=self.ALPHABETS,
            transitions=self.TRANSACTIONS,
            start_state=self.START_STATE,
            accept_states=self.ACCEPT_STATES
        )
        new_dfa = dfa.minimize()

        self.lbl_result_inital_state.setText(new_dfa.start_state)
        self.lbl_result_final_state.setText(" & ".join(new_dfa.accept_states))
        
        self.listWidget_MinimizeTab_StateName.clear()
        self.listWidget_MinimizeTab_StateName.addItems(new_dfa.states)

        self.listWidget_MinimizeTab_Alphabet.clear()
        self.listWidget_MinimizeTab_Alphabet.addItems(new_dfa.alphabet)

        self.tableWidget_Minimize_Transaction.setRowCount(len(new_dfa.transitions))
        for row_index, ((current_state, transaction), target_state) in enumerate(new_dfa.transitions.items()):
            self.tableWidget_Minimize_Transaction.setItem(row_index, 0, QTableWidgetItem(current_state))
            self.tableWidget_Minimize_Transaction.setItem(row_index, 1, QTableWidgetItem(transaction))
            self.tableWidget_Minimize_Transaction.setItem(row_index, 2, QTableWidgetItem(target_state))


    def on_btn_EquivalentTab_State_Add(self):
        user_input = self.txt_EquivalentTab_State_StateName.toPlainText()
        if user_input != "":
            if user_input not in self.STATES_1:
                if self.cb_EquivalentTab_finall_state.isChecked() == True:
                    self.ACCEPT_STATES_1.append(self.txt_EquivalentTab_State_StateName.toPlainText())
                self.STATES_1.append(self.txt_EquivalentTab_State_StateName.toPlainText())
                self.listWidget_EquivalentTab_State_StateName.addItem(self.STATES_1[-1])
                self.update_initial_and_final_state()


    def on_btn_EquivalentTab_add_Alphabet(self):
        user_input = self.txt_EquivalentTab_Alphabet.toPlainText()
        if len(user_input) == 1:
            if user_input not in self.ALPHABETS_1:
                self.ALPHABETS_1.append(user_input)
                self.listWidget_EquivalentTab_Alphabet.addItem(self.ALPHABETS_1[-1])
    
    def remove_EquivalentTab_selected_item_listwidget_states(self):
        selected_items = self.listWidget_EquivalentTab_State_StateName.selectedItems()
        for item in selected_items:
            row = self.listWidget_EquivalentTab_State_StateName.row(item)
            self.STATES_1.remove(item.text())
            if item.text() in self.ACCEPT_STATES_1:
                self.ACCEPT_STATES_1.remove(item.text())
            self.listWidget_EquivalentTab_State_StateName.takeItem(row)
            del item
            self.update_initial_and_final_state()

    def remove_EquivalentTab_selected_item_listwidget_alphabet(self):
        selected_items = self.listWidget_EquivalentTab_Alphabet.selectedItems()

        for item in selected_items:
            row = self.listWidget_EquivalentTab_Alphabet.row(item)
            self.ALPHABETS_1.remove(item.text())
            self.listWidget_EquivalentTab_Alphabet.takeItem(row)
            del item

    def on_page_EquivalentTab_Transaction_shown(self, event):
        self.combo_CurrentStates_3.clear()
        self.combo_Transactions_3.clear()
        self.combo_TargetStates_3.clear()

        self.combo_CurrentStates_3.addItems(self.STATES_1)
        self.combo_Transactions_3.addItems(self.ALPHABETS_1)
        self.combo_TargetStates_3.addItems(self.STATES_1)

        self.populate_table_EquivalentTab()

    def on_btn_EquivalentTab_add_Transaction(self):
        current_state = self.combo_CurrentStates_3.currentText()
        transaction = self.combo_Transactions_3.currentText()
        target_state = self.combo_TargetStates_3.currentText()

        self.TRANSACTIONS_1[(current_state, transaction)] = target_state
        self.populate_table_EquivalentTab()


    def populate_table_EquivalentTab(self):
        self.tableWidget_EquivalentTab_Transaction.setRowCount(len(self.TRANSACTIONS_1))
        for row_index, ((current_state, transaction), target_state) in enumerate(self.TRANSACTIONS_1.items()):
            self.tableWidget_EquivalentTab_Transaction.setItem(row_index, 0, QTableWidgetItem(current_state))
            self.tableWidget_EquivalentTab_Transaction.setItem(row_index, 1, QTableWidgetItem(transaction))
            self.tableWidget_EquivalentTab_Transaction.setItem(row_index, 2, QTableWidgetItem(target_state))


    def on_btn_Equivalent(self):
        self.START_STATE = self.combo_InitialState.currentText()
        self.START_STATE_1 = self.combo_Equivalent_InitialState.currentText()
        dfa = Dfa(
            states=self.STATES,
            alphabet=self.ALPHABETS,
            transitions=self.TRANSACTIONS,
            start_state=self.START_STATE,
            accept_states=self.ACCEPT_STATES
        ) 
        dfa_1 = Dfa(
            states=self.STATES_1,
            alphabet=self.ALPHABETS_1,
            transitions=self.TRANSACTIONS_1,
            start_state=self.START_STATE_1,
            accept_states=self.ACCEPT_STATES_1
        )       
        result_str = f"{self.txt_DFAName_2.toPlainText()} and {self.txt_Equivalent_DFAName.toPlainText()} "
        result_bool = dfa.are_equivalent(dfa_1)
        if result_bool:
            self.lbl_result_is_Equivalent.setText(result_str + "are equivalent")
        else:
            self.lbl_result_is_Equivalent.setText(result_str + "aren't equivalent")



    def on_btn_Save_Expression_1(self):

        self.listWidget_RE_DFATab_StateName.clear()
        self.listWidget_RE_DFATab_Alphabet.clear()
        self.tableWidget_RE_DFATab_Transaction.clear()
        self.listWidget_RE_NFATab_StateName.clear()
        self.listWidget_RE_NFATab_Alphabet.clear()
        self.tableWidget_RE_NFATab_Transaction.clear()

        regex_analyzer = RegularExpressionAnalyzer()
        input_user = self.txt_Expression_1.toPlainText()
        self.Expression_1 = input_user
        if regex_analyzer.is_regular(input_user):
            self.lbl_result_is_regular_language.setText("Yes, Is regular")
            result_dfa = regex_analyzer.to_dfa(input_user)

            degree = Degree(input_user).get_degree()
            self.lbl_result_degree.setText(str(degree))
            
            start_state_list = []
            for i in result_dfa.start_state:
                if type(i) is tuple or set:
                    start_state_list.append(", ".join(i))
                else:
                    start_state_list.append(i)

            final_state_list = []
            for i in result_dfa.accept_states:
                if type(i) is tuple or set:
                    final_state_list.append(", ".join(i))
                else:
                    final_state_list.append(i)
            self.lbl_result_DFA_inital_state.setText(" & ".join(start_state_list))
            self.lbl_result_DFA_final_state.setText(" & ".join(final_state_list))

            for i in list(result_dfa.states):
                self.listWidget_RE_DFATab_StateName.addItem(", ".join(i))
            #self.listWidget_RE_DFATab_StateName.addItems(list(result_dfa.states))
            self.listWidget_RE_DFATab_Alphabet.addItems(list(result_dfa.alphabet))
            transitions = self.modify_dictionary_transaction(result_dfa.transitions)
            self.tableWidget_RE_DFATab_Transaction.setRowCount(len(transitions))
            for row_index, ((current_state, transaction), target_state) in enumerate(transitions.items()):
                self.tableWidget_RE_DFATab_Transaction.setItem(row_index, 0, QTableWidgetItem(current_state))
                self.tableWidget_RE_DFATab_Transaction.setItem(row_index, 1, QTableWidgetItem(transaction))
                self.tableWidget_RE_DFATab_Transaction.setItem(row_index, 2, QTableWidgetItem(target_state))
        else:
            self.lbl_result_is_regular_language.setText("No, Isn't regular")
        result_nfa = regex_analyzer.to_nfa(input_user)



        start_state_list = []
        for i in result_nfa.start_state:
            if type(i) is tuple or set:
                start_state_list.append(", ".join(i))
            else:
                start_state_list.append(i)

        final_state_list = []
        for i in result_nfa.accept_states:
            if type(i) is tuple or set:
                final_state_list.append(", ".join(i))
            else:
                final_state_list.append(i)
        self.lbl_result_NFA_inital_state.setText(" & ".join(start_state_list))
        self.lbl_result_NFA_final_state.setText(" & ".join(final_state_list))
        # for i in list(result_nfa.states):
        #     self.listWidget_RE_NFATab_StateName.addItem(i)
        self.listWidget_RE_NFATab_StateName.addItems(list(result_nfa.states))
        self.listWidget_RE_NFATab_Alphabet.addItems(list(result_nfa.alphabet))
        transitions = self.modify_dictionary_transaction(result_nfa.transitions)
        self.tableWidget_RE_NFATab_Transaction.setRowCount(len(transitions))
        for row_index, ((current_state, transaction), target_state) in enumerate(transitions.items()):
            self.tableWidget_RE_NFATab_Transaction.setItem(row_index, 0, QTableWidgetItem(current_state))
            self.tableWidget_RE_NFATab_Transaction.setItem(row_index, 1, QTableWidgetItem(transaction))
            self.tableWidget_RE_NFATab_Transaction.setItem(row_index, 2, QTableWidgetItem(target_state))

    def modify_dictionary_transaction(self, entry_transitions):
        transitions = {}
        for current_states, transitions_dict in entry_transitions.items():
            if len(current_states) != 1:
                    current_states = ", ".join(current_states)
            else:
                current_states = str(current_states[0])
            for symbol, next_state in transitions_dict.items():
                if len(next_state) != 1:
                    next_state = ", ".join(next_state)
                else:
                    next_state = str(next_state[0])      
                transitions[(current_states, symbol)] = next_state
        return transitions
    
    def on_btn_Save_Expression_2(self):
        self.Expression_2 = self.txt_Expression_2.toPlainText()
        regex_analyzer = RegularExpressionAnalyzer()
        if regex_analyzer.is_regular(self.Expression_1) and regex_analyzer.is_regular(self.Expression_2):
            if regex_analyzer.compare_languages(self.Expression_1, self.Expression_2):
                self.lbl_result_Are_languages_equvalent.setText("Yes")
            else:
                self.lbl_result_Are_languages_equvalent.setText("No")

            if regex_analyzer.is_relation(self.Expression_1, self.Expression_2):
                self.lbl_result_is_there_a_relation.setText("Yes")
            else:
                self.lbl_result_is_there_a_relation.setText("No")
                
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1082, 758)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 10, 1071, 731))
        self.DFA_tab = QWidget()
        self.DFA_tab.setObjectName(u"DFA_tab")
        self.groupBox = QGroupBox(self.DFA_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 10, 1031, 681))
        self.toolBox = QToolBox(self.groupBox)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setGeometry(QRect(10, 30, 301, 461))
        self.tool_box_state = QWidget()
        self.tool_box_state.setObjectName(u"tool_box_state")
        self.tool_box_state.setGeometry(QRect(0, 0, 301, 380))
        self.scrollArea = QScrollArea(self.tool_box_state)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 10, 301, 361))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 299, 359))
        self.grb_StateName = QGroupBox(self.scrollAreaWidgetContents)
        self.grb_StateName.setObjectName(u"grb_StateName")
        self.grb_StateName.setGeometry(QRect(30, 20, 241, 141))
        self.txt_StateName = QTextEdit(self.grb_StateName)
        self.txt_StateName.setObjectName(u"txt_StateName")
        self.txt_StateName.setGeometry(QRect(20, 30, 201, 31))
        self.btn_add_StateName = QPushButton(self.grb_StateName)
        self.btn_add_StateName.setObjectName(u"btn_add_StateName")
        self.btn_add_StateName.setGeometry(QRect(80, 110, 75, 23))
        self.cb_finall_state = QCheckBox(self.grb_StateName)
        self.cb_finall_state.setObjectName(u"cb_finall_state")
        self.cb_finall_state.setGeometry(QRect(30, 70, 70, 17))
        self.listWidget_StatesName = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_StatesName.setObjectName(u"listWidget_StatesName")
        self.listWidget_StatesName.setGeometry(QRect(30, 180, 241, 111))
        self.btn_remove_StateName = QPushButton(self.scrollAreaWidgetContents)
        self.btn_remove_StateName.setObjectName(u"btn_remove_StateName")
        self.btn_remove_StateName.setGeometry(QRect(110, 300, 75, 23))

        self.btn_add_StateName.clicked.connect(self.on_btn_add_StateName)
        self.btn_remove_StateName.clicked.connect(self.remove_selected_item_listwidget_states)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.toolBox.addItem(self.tool_box_state, u"State")
        self.page_Alphabet = QWidget()
        self.page_Alphabet.setObjectName(u"page_Alphabet")
        self.page_Alphabet.setGeometry(QRect(0, 0, 301, 380))
        self.scrollArea_2 = QScrollArea(self.page_Alphabet)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(0, 10, 301, 361))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 299, 359))
        self.grb_StateName_2 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.grb_StateName_2.setObjectName(u"grb_StateName_2")
        self.grb_StateName_2.setGeometry(QRect(30, 30, 241, 101))
        self.txt_Alphabet = QTextEdit(self.grb_StateName_2)
        self.txt_Alphabet.setObjectName(u"txt_Alphabet")
        self.txt_Alphabet.setGeometry(QRect(20, 30, 201, 31))
        self.btn_add_Alphabet = QPushButton(self.grb_StateName_2)
        self.btn_add_Alphabet.setObjectName(u"btn_add_Alphabet")
        self.btn_add_Alphabet.setGeometry(QRect(80, 70, 75, 23))
        self.listWidget_Alphabet = QListWidget(self.scrollAreaWidgetContents_2)
        self.listWidget_Alphabet.setObjectName(u"listWidget_Alphabet")
        self.listWidget_Alphabet.setGeometry(QRect(30, 170, 241, 121))
        self.btn_remove_Alphabet = QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_remove_Alphabet.setObjectName(u"btn_remove_Alphabet")
        self.btn_remove_Alphabet.setGeometry(QRect(110, 300, 75, 23))

        self.btn_add_Alphabet.clicked.connect(self.on_btn_add_Alphabet)
        self.btn_remove_Alphabet.clicked.connect(self.remove_selected_item_listwidget_alphabet)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.toolBox.addItem(self.page_Alphabet, u"Alphabet")
        self.page_Transaction = QWidget()
        self.page_Transaction.setObjectName(u"page_Transaction")

        self.page_Transaction.showEvent = lambda event: self.on_page_Transaction_shown(event)

        self.scrollArea_3 = QScrollArea(self.page_Transaction)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setGeometry(QRect(0, 0, 301, 371))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 299, 369))
        self.grb_StateName_3 = QGroupBox(self.scrollAreaWidgetContents_3)
        self.grb_StateName_3.setObjectName(u"grb_StateName_3")
        self.grb_StateName_3.setGeometry(QRect(30, 30, 241, 111))
        self.combo_CurrentStates = QComboBox(self.grb_StateName_3)
        self.combo_CurrentStates.setObjectName(u"combo_CurrentStates")
        self.combo_CurrentStates.setGeometry(QRect(110, 20, 121, 22))
        self.combo_Transactions = QComboBox(self.grb_StateName_3)
        self.combo_Transactions.setObjectName(u"combo_Transactions")
        self.combo_Transactions.setGeometry(QRect(110, 50, 121, 22))
        self.label = QLabel(self.grb_StateName_3)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 71, 16))
        self.combo_TargetStates = QComboBox(self.grb_StateName_3)
        self.combo_TargetStates.setObjectName(u"combo_TargetStates")
        self.combo_TargetStates.setGeometry(QRect(110, 80, 121, 22))
        self.label_2 = QLabel(self.grb_StateName_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 50, 71, 16))
        self.label_3 = QLabel(self.grb_StateName_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 80, 71, 16))

        self.btn_add_Transaction = QPushButton(self.scrollAreaWidgetContents_3)
        self.btn_add_Transaction.setObjectName(u"btn_add_Transaction")
        self.btn_add_Transaction.setGeometry(QRect(110, 150, 75, 23))

        self.btn_add_Transaction.clicked.connect(self.on_btn_add_Transaction)

        self.tableWidget_Transaction = QTableWidget(self.scrollAreaWidgetContents_3)
        if (self.tableWidget_Transaction.columnCount() < 3):
            self.tableWidget_Transaction.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_Transaction.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_Transaction.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_Transaction.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget_Transaction.setObjectName(u"tableWidget_Transaction")
        self.tableWidget_Transaction.setGeometry(QRect(30, 210, 241, 111))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.toolBox.addItem(self.page_Transaction, u"Transaction")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 540, 61, 16))
        self.combo_InitialState = QComboBox(self.groupBox)
        self.combo_InitialState.setObjectName(u"combo_InitialState")
        self.combo_InitialState.setGeometry(QRect(130, 540, 121, 22))
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(340, 20, 681, 641))
        font = QFont()
        font.setFamily(u"Microsoft Sans Serif")
        self.groupBox_2.setFont(font)
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 20, 191, 51))
        font1 = QFont()
        font1.setFamily(u"Microsoft Sans Serif")
        font1.setPointSize(12)
        self.label_6.setFont(font1)
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 70, 191, 51))
        self.label_7.setFont(font1)
        self.txt_DFAName = QToolBox(self.groupBox_2)
        self.txt_DFAName.setObjectName(u"txt_DFAName")
        self.txt_DFAName.setGeometry(QRect(20, 132, 641, 501))        
        font2 = QFont()
        font2.setFamily(u"MS Shell Dlg 2")
        font2.setPointSize(12)
        self.txt_DFAName.setFont(font2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 641, 402))
        self.label_9 = QLabel(self.page)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(220, 60, 201, 51))
        font3 = QFont()
        font3.setFamily(u"MS Shell Dlg 2")
        font3.setPointSize(10)
        self.label_9.setFont(font3)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.textEdit_2 = QTextEdit(self.page)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setEnabled(True)
        self.textEdit_2.setGeometry(QRect(210, 110, 221, 31))
        font4 = QFont()
        font4.setFamily(u"MS Shell Dlg 2")
        font4.setPointSize(12)
        font4.setKerning(True)
        self.textEdit_2.setFont(font4)
        self.textEdit_2.setMouseTracking(False)
        self.textEdit_2.setAutoFillBackground(False)
        self.textEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setUndoRedoEnabled(True)
        self.pushButton_2 = QPushButton(self.page)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(260, 160, 121, 31))

        self.pushButton_2.clicked.connect(self.on_test_string)

        font5 = QFont()
        font5.setFamily(u"Microsoft Sans Serif")
        font5.setPointSize(14)
        self.pushButton_2.setFont(font5)
        self.lbl_result_test_string = QLabel(self.page)
        self.lbl_result_test_string.setObjectName(u"lbl_result_test_string")
        self.lbl_result_test_string.setGeometry(QRect(270, 250, 101, 51))
        font6 = QFont()
        font6.setFamily(u"Microsoft Sans Serif")
        font6.setPointSize(12)
        font6.setBold(False)
        font6.setWeight(50)
        self.lbl_result_test_string.setFont(font6)
        self.lbl_result_test_string.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_test_string.setAlignment(Qt.AlignCenter)
        self.txt_DFAName.addItem(self.page, u"Test string")
        self.Minimize = QWidget()
        self.Minimize.setObjectName(u"Minimize")
        self.Minimize.setGeometry(QRect(0, 0, 641, 402))
        self.toolBox_3 = QToolBox(self.Minimize)
        self.toolBox_3.setObjectName(u"toolBox_3")
        self.toolBox_3.setGeometry(QRect(30, 0, 581, 251))

        self.toolBox_3.showEvent = lambda event: self.on_page_Minimize_shown(event)

        font7 = QFont()
        font7.setFamily(u"Microsoft Sans Serif")
        font7.setPointSize(8)
        self.toolBox_3.setFont(font7)
        self.tool_box_state_3 = QWidget()
        self.tool_box_state_3.setObjectName(u"tool_box_state_3")
        self.tool_box_state_3.setGeometry(QRect(0, 0, 581, 170))
        self.scrollArea_7 = QScrollArea(self.tool_box_state_3)
        self.scrollArea_7.setObjectName(u"scrollArea_7")
        self.scrollArea_7.setGeometry(QRect(0, 20, 581, 121))
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName(u"scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, 0, 579, 119))
        self.grb_StateName_7 = QGroupBox(self.scrollAreaWidgetContents_7)
        self.grb_StateName_7.setObjectName(u"grb_StateName_7")
        self.grb_StateName_7.setGeometry(QRect(30, 10, 531, 91))
        self.grb_StateName_7.setFont(font7)
        self.listWidget_MinimizeTab_StateName = QListWidget(self.grb_StateName_7)
        self.listWidget_MinimizeTab_StateName.setObjectName(u"listWidget_MinimizeTab_StateName")
        self.listWidget_MinimizeTab_StateName.setGeometry(QRect(10, 20, 511, 61))
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)
        self.toolBox_3.addItem(self.tool_box_state_3, u"State")
        self.page_Alphabet_3 = QWidget()
        self.page_Alphabet_3.setObjectName(u"page_Alphabet_3")
        self.page_Alphabet_3.setGeometry(QRect(0, 0, 581, 170))
        self.scrollArea_8 = QScrollArea(self.page_Alphabet_3)
        self.scrollArea_8.setObjectName(u"scrollArea_8")
        self.scrollArea_8.setGeometry(QRect(0, 10, 581, 141))
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setObjectName(u"scrollAreaWidgetContents_8")
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, 0, 579, 139))
        self.grb_StateName_8 = QGroupBox(self.scrollAreaWidgetContents_8)
        self.grb_StateName_8.setObjectName(u"grb_StateName_8")
        self.grb_StateName_8.setGeometry(QRect(10, 10, 561, 121))
        self.listWidget_MinimizeTab_Alphabet = QListWidget(self.grb_StateName_8)
        self.listWidget_MinimizeTab_Alphabet.setObjectName(u"listWidget_MinimizeTab_Alphabet")
        self.listWidget_MinimizeTab_Alphabet.setGeometry(QRect(0, 0, 561, 121))
        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)
        self.toolBox_3.addItem(self.page_Alphabet_3, u"Alphabet")
        self.page_Transaction_3 = QWidget()
        self.page_Transaction_3.setObjectName(u"page_Transaction_3")
        self.page_Transaction_3.setGeometry(QRect(0, 0, 581, 170))
        self.scrollArea_9 = QScrollArea(self.page_Transaction_3)
        self.scrollArea_9.setObjectName(u"scrollArea_9")
        self.scrollArea_9.setGeometry(QRect(0, 0, 581, 161))
        self.scrollArea_9.setWidgetResizable(True)
        self.scrollAreaWidgetContents_9 = QWidget()
        self.scrollAreaWidgetContents_9.setObjectName(u"scrollAreaWidgetContents_9")
        self.scrollAreaWidgetContents_9.setGeometry(QRect(0, 0, 579, 159))
        self.tableWidget_Minimize_Transaction = QTableWidget(self.scrollAreaWidgetContents_9)
        if (self.tableWidget_Minimize_Transaction.columnCount() < 3):
            self.tableWidget_Minimize_Transaction.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_Minimize_Transaction.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_Minimize_Transaction.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_Minimize_Transaction.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidget_Minimize_Transaction.setObjectName(u"tableWidget_Minimize_Transaction")
        self.tableWidget_Minimize_Transaction.setGeometry(QRect(0, 0, 581, 161))
        self.scrollArea_9.setWidget(self.scrollAreaWidgetContents_9)
        self.toolBox_3.addItem(self.page_Transaction_3, u"Transaction")

        self.label_20 = QLabel(self.Minimize)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(190, 270, 81, 51))
        self.label_20.setFont(font1)
        self.label_21 = QLabel(self.Minimize)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(190, 310, 91, 51))
        self.label_21.setFont(font1)
        self.lbl_result_inital_state = QLabel(self.Minimize)
        self.lbl_result_inital_state.setObjectName(u"lbl_result_inital_state")
        self.lbl_result_inital_state.setGeometry(QRect(350, 270, 261, 51))
        self.lbl_result_inital_state.setFont(font1)
        self.lbl_result_final_state = QLabel(self.Minimize)
        self.lbl_result_final_state.setObjectName(u"lbl_result_final_state")
        self.lbl_result_final_state.setGeometry(QRect(350, 310, 261, 51))
        self.lbl_result_final_state.setFont(font1)


        self.txt_DFAName.addItem(self.Minimize, u"Minimize")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 641, 402))
        self.toolBox_4 = QToolBox(self.page_2)
        self.toolBox_4.setObjectName(u"toolBox_4")
        self.toolBox_4.setGeometry(QRect(20, 10, 601, 241))
        self.toolBox_4.setFont(font7)
        self.tool_box_state_4 = QWidget()
        self.tool_box_state_4.setObjectName(u"tool_box_state_4")
        self.tool_box_state_4.setGeometry(QRect(0, 0, 601, 160))
        self.scrollArea_10 = QScrollArea(self.tool_box_state_4)
        self.scrollArea_10.setObjectName(u"scrollArea_10")
        self.scrollArea_10.setGeometry(QRect(0, 20, 601, 131))
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_10 = QWidget()
        self.scrollAreaWidgetContents_10.setObjectName(u"scrollAreaWidgetContents_10")
        self.scrollAreaWidgetContents_10.setGeometry(QRect(0, 0, 599, 129))
        self.grb_StateName_9 = QGroupBox(self.scrollAreaWidgetContents_10)
        self.grb_StateName_9.setObjectName(u"grb_StateName_9")
        self.grb_StateName_9.setGeometry(QRect(120, 10, 181, 121))
        self.txt_EquivalentTab_State_StateName = QTextEdit(self.grb_StateName_9)
        self.txt_EquivalentTab_State_StateName.setObjectName(u"txt_EquivalentTab_State_StateName")
        self.txt_EquivalentTab_State_StateName.setGeometry(QRect(20, 30, 141, 31))
        self.btn_EquivalentTab_State_Add = QPushButton(self.grb_StateName_9)
        self.btn_EquivalentTab_State_Add.setObjectName(u"btn_EquivalentTab_State_Add")
        self.btn_EquivalentTab_State_Add.setGeometry(QRect(50, 90, 75, 23))
        self.cb_EquivalentTab_finall_state = QCheckBox(self.grb_StateName_9)
        self.cb_EquivalentTab_finall_state.setObjectName(u"cb_EquivalentTab_finall_state")
        self.cb_EquivalentTab_finall_state.setGeometry(QRect(30, 70, 70, 17))
        self.listWidget_EquivalentTab_State_StateName = QListWidget(self.scrollAreaWidgetContents_10)
        self.listWidget_EquivalentTab_State_StateName.setObjectName(u"listWidget_EquivalentTab_State_StateName")
        self.listWidget_EquivalentTab_State_StateName.setGeometry(QRect(310, 20, 161, 51))
        self.btn_EquivalentTab_State_Remove = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_EquivalentTab_State_Remove.setObjectName(u"btn_EquivalentTab_State_Remove")
        self.btn_EquivalentTab_State_Remove.setGeometry(QRect(350, 80, 75, 23))

        self.btn_EquivalentTab_State_Add.clicked.connect(self.on_btn_EquivalentTab_State_Add)
        self.btn_EquivalentTab_State_Remove.clicked.connect(self.remove_EquivalentTab_selected_item_listwidget_states)

        self.scrollArea_10.setWidget(self.scrollAreaWidgetContents_10)
        self.toolBox_4.addItem(self.tool_box_state_4, u"State")
        self.page_Alphabet_4 = QWidget()
        self.page_Alphabet_4.setObjectName(u"page_Alphabet_4")
        self.page_Alphabet_4.setGeometry(QRect(0, 0, 601, 160))
        self.scrollArea_11 = QScrollArea(self.page_Alphabet_4)
        self.scrollArea_11.setObjectName(u"scrollArea_11")
        self.scrollArea_11.setGeometry(QRect(0, 10, 601, 131))
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName(u"scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 599, 129))
        self.grb_StateName_10 = QGroupBox(self.scrollAreaWidgetContents_11)
        self.grb_StateName_10.setObjectName(u"grb_StateName_10")
        self.grb_StateName_10.setGeometry(QRect(130, 10, 181, 101))
        self.txt_EquivalentTab_Alphabet = QTextEdit(self.grb_StateName_10)
        self.txt_EquivalentTab_Alphabet.setObjectName(u"txt_EquivalentTab_Alphabet")
        self.txt_EquivalentTab_Alphabet.setGeometry(QRect(20, 30, 141, 31))
        self.btn_EquivalentTab_Alphabet_Add = QPushButton(self.grb_StateName_10)
        self.btn_EquivalentTab_Alphabet_Add.setObjectName(u"btn_EquivalentTab_Alphabet_Add")
        self.btn_EquivalentTab_Alphabet_Add.setGeometry(QRect(50, 70, 75, 23))
        self.btn_EquivalentTab_Alphabet_Remove = QPushButton(self.scrollAreaWidgetContents_11)
        self.btn_EquivalentTab_Alphabet_Remove.setObjectName(u"btn_EquivalentTab_Alphabet_Remove")
        self.btn_EquivalentTab_Alphabet_Remove.setGeometry(QRect(360, 80, 75, 23))
        self.listWidget_EquivalentTab_Alphabet = QListWidget(self.scrollAreaWidgetContents_11)
        self.listWidget_EquivalentTab_Alphabet.setObjectName(u"listWidget_EquivalentTab_Alphabet")
        self.listWidget_EquivalentTab_Alphabet.setGeometry(QRect(320, 20, 161, 51))
        
        self.btn_EquivalentTab_Alphabet_Add.clicked.connect(self.on_btn_EquivalentTab_add_Alphabet)
        self.btn_EquivalentTab_Alphabet_Remove.clicked.connect(self.remove_EquivalentTab_selected_item_listwidget_alphabet)
        
        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_11)
        self.toolBox_4.addItem(self.page_Alphabet_4, u"Alphabet")
        self.page_Transaction_4 = QWidget()
        self.page_Transaction_4.setObjectName(u"page_Transaction_4")
        self.page_Transaction_4.setGeometry(QRect(0, 0, 601, 160))

        self.page_Transaction_4.showEvent = lambda event: self.on_page_EquivalentTab_Transaction_shown(event)

        self.scrollArea_12 = QScrollArea(self.page_Transaction_4)
        self.scrollArea_12.setObjectName(u"scrollArea_12")
        self.scrollArea_12.setGeometry(QRect(0, 0, 601, 151))
        self.scrollArea_12.setWidgetResizable(True)
        self.scrollAreaWidgetContents_12 = QWidget()
        self.scrollAreaWidgetContents_12.setObjectName(u"scrollAreaWidgetContents_12")
        self.scrollAreaWidgetContents_12.setGeometry(QRect(0, 0, 599, 149))
        self.tableWidget_EquivalentTab_Transaction = QTableWidget(self.scrollAreaWidgetContents_12)
        if (self.tableWidget_EquivalentTab_Transaction.columnCount() < 3):
            self.tableWidget_EquivalentTab_Transaction.setColumnCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_EquivalentTab_Transaction.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_EquivalentTab_Transaction.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_EquivalentTab_Transaction.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        self.tableWidget_EquivalentTab_Transaction.setObjectName(u"tableWidget_EquivalentTab_Transaction")
        self.tableWidget_EquivalentTab_Transaction.setGeometry(QRect(270, 10, 311, 111))
        self.btn_add_Transaction_3 = QPushButton(self.scrollAreaWidgetContents_12)
        self.btn_add_Transaction_3.setObjectName(u"btn_add_Transaction_3")
        self.btn_add_Transaction_3.setGeometry(QRect(90, 120, 75, 23))

        self.btn_add_Transaction_3.clicked.connect(self.on_btn_EquivalentTab_add_Transaction)
        
        self.grb_StateName_11 = QGroupBox(self.scrollAreaWidgetContents_12)
        self.grb_StateName_11.setObjectName(u"grb_StateName_11")
        self.grb_StateName_11.setGeometry(QRect(20, 10, 221, 111))
        self.combo_CurrentStates_3 = QComboBox(self.grb_StateName_11)
        self.combo_CurrentStates_3.setObjectName(u"combo_CurrentStates_3")
        self.combo_CurrentStates_3.setGeometry(QRect(110, 20, 101, 22))
        self.combo_Transactions_3 = QComboBox(self.grb_StateName_11)
        self.combo_Transactions_3.setObjectName(u"combo_Transactions_3")
        self.combo_Transactions_3.setGeometry(QRect(110, 50, 101, 22))
        self.label_13 = QLabel(self.grb_StateName_11)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(20, 20, 71, 16))
        self.combo_TargetStates_3 = QComboBox(self.grb_StateName_11)
        self.combo_TargetStates_3.setObjectName(u"combo_TargetStates_3")
        self.combo_TargetStates_3.setGeometry(QRect(110, 80, 101, 22))
        self.label_17 = QLabel(self.grb_StateName_11)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 50, 71, 16))
        self.label_18 = QLabel(self.grb_StateName_11)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(20, 80, 71, 16))
        self.scrollArea_12.setWidget(self.scrollAreaWidgetContents_12)
        self.toolBox_4.addItem(self.page_Transaction_4, u"Transaction")
        self.label_10 = QLabel(self.page_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(30, 280, 61, 16))
        font8 = QFont()
        font8.setFamily(u"MS Shell Dlg 2")
        font8.setPointSize(8)
        self.label_10.setFont(font8)
        self.label_12 = QLabel(self.page_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(30, 320, 61, 16))
        self.label_12.setFont(font8)
        self.combo_Equivalent_InitialState = QComboBox(self.page_2)
        self.combo_Equivalent_InitialState.setObjectName(u"combo_Equivalent_InitialState")
        self.combo_Equivalent_InitialState.setGeometry(QRect(100, 280, 121, 22))
        self.combo_Equivalent_InitialState.setFont(font8)
        self.txt_Equivalent_DFAName = QTextEdit(self.page_2)
        self.txt_Equivalent_DFAName.setObjectName(u"txt_Equivalent_DFAName")
        self.txt_Equivalent_DFAName.setEnabled(True)
        self.txt_Equivalent_DFAName.setGeometry(QRect(100, 320, 121, 21))
        self.txt_Equivalent_DFAName.setFont(font8)
        self.txt_Equivalent_DFAName.setMouseTracking(False)
        self.txt_Equivalent_DFAName.setAutoFillBackground(False)
        self.txt_Equivalent_DFAName.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_Equivalent_DFAName.setUndoRedoEnabled(True)
        self.btn_Equivalent = QPushButton(self.page_2)
        self.btn_Equivalent.setObjectName(u"btn_Equivalent")
        self.btn_Equivalent.setGeometry(QRect(70, 360, 111, 31))
        self.btn_Equivalent.setFont(font8)

        self.btn_Equivalent.clicked.connect(self.on_btn_Equivalent)

        self.lbl_result_is_Equivalent = QLabel(self.page_2)
        self.lbl_result_is_Equivalent.setObjectName(u"lbl_result_is_Equivalent")
        self.lbl_result_is_Equivalent.setGeometry(QRect(280, 300, 321, 51))
        self.lbl_result_is_Equivalent.setFont(font6)
        self.lbl_result_is_Equivalent.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_is_Equivalent.setAlignment(Qt.AlignCenter)
        self.txt_DFAName.addItem(self.page_2, u"Equivalent")
        self.lbl_result_is_empty_language = QLabel(self.groupBox_2)
        self.lbl_result_is_empty_language.setObjectName(u"lbl_result_is_empty_language")
        self.lbl_result_is_empty_language.setGeometry(QRect(160, 20, 121, 51))
        self.lbl_result_is_empty_language.setFont(font6)
        self.lbl_result_is_empty_language.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_is_empty_language.setAlignment(Qt.AlignCenter)
        self.lbl_result_is_finite = QLabel(self.groupBox_2)
        self.lbl_result_is_finite.setObjectName(u"lbl_result_is_finite")
        self.lbl_result_is_finite.setGeometry(QRect(160, 70, 121, 51))
        self.lbl_result_is_finite.setFont(font6)
        self.lbl_result_is_finite.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_is_finite.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(260, 20, 191, 51))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignCenter)
        self.lbl_result_allStrings = QLabel(self.groupBox_2)
        self.lbl_result_allStrings.setObjectName(u"lbl_result_allStrings")
        self.lbl_result_allStrings.setGeometry(QRect(450, 40, 101, 16))
        self.lbl_result_allStrings.setFont(font6)
        self.lbl_result_allStrings.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_allStrings.setAlignment(Qt.AlignCenter)
        self.listWidget_AllString = QListWidget(self.groupBox_2)
        self.listWidget_AllString.setObjectName(u"listWidget_AllString")
        self.listWidget_AllString.setGeometry(QRect(420, 70, 161, 51))
        self.txt_DFAName_2 = QTextEdit(self.groupBox)
        self.txt_DFAName_2.setObjectName(u"txt_DFAName_2")
        self.txt_DFAName_2.setEnabled(True)
        self.txt_DFAName_2.setGeometry(QRect(130, 580, 121, 21))
        font9 = QFont()
        font9.setKerning(True)
        self.txt_DFAName_2.setFont(font9)
        self.txt_DFAName_2.setMouseTracking(False)
        self.txt_DFAName_2.setAutoFillBackground(False)
        self.txt_DFAName_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_DFAName_2.setUndoRedoEnabled(True)
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(60, 580, 61, 16))
        self.btn_Save = QPushButton(self.groupBox)
        self.btn_Save.setObjectName(u"btn_Save")
        self.btn_Save.setGeometry(QRect(100, 620, 111, 31))

        self.btn_Save.clicked.connect(self.on_btn_save)

        self.tabWidget.addTab(self.DFA_tab, "")
        self.regular_language_tab = QWidget()
        self.regular_language_tab.setObjectName(u"regular_language_tab")


        self.groupBox_3 = QGroupBox(self.regular_language_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(19, 9, 1031, 691))
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(310, 40, 191, 51))
        self.label_5.setFont(font1)
        self.txt_Expression_1 = QTextEdit(self.groupBox_3)
        self.txt_Expression_1.setObjectName(u"txt_Expression_1")
        self.txt_Expression_1.setEnabled(True)
        self.txt_Expression_1.setGeometry(QRect(410, 50, 231, 31))
        self.txt_Expression_1.setFont(font4)
        self.txt_Expression_1.setMouseTracking(False)
        self.txt_Expression_1.setAutoFillBackground(False)
        self.txt_Expression_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_Expression_1.setUndoRedoEnabled(True)
        self.btn_Save_Expression_1 = QPushButton(self.groupBox_3)
        self.btn_Save_Expression_1.setObjectName(u"btn_Save_Expression_1")
        self.btn_Save_Expression_1.setGeometry(QRect(470, 110, 111, 31))

        self.btn_Save_Expression_1.clicked.connect(self.on_btn_Save_Expression_1)

        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(310, 180, 191, 51))
        self.label_14.setFont(font1)
        self.lbl_result_is_regular_language = QLabel(self.groupBox_3)
        self.lbl_result_is_regular_language.setObjectName(u"lbl_result_is_regular_language")
        self.lbl_result_is_regular_language.setGeometry(QRect(570, 180, 121, 51))
        self.lbl_result_is_regular_language.setFont(font6)
        self.lbl_result_is_regular_language.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_is_regular_language.setAlignment(Qt.AlignCenter)
        self.toolBox_2 = QToolBox(self.groupBox_3)
        self.toolBox_2.setObjectName(u"toolBox_2")
        self.toolBox_2.setGeometry(QRect(150, 260, 751, 391))
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 751, 310))
        self.toolBox_5 = QToolBox(self.page_3)
        self.toolBox_5.setObjectName(u"toolBox_5")
        self.toolBox_5.setGeometry(QRect(60, 0, 611, 261))
        self.toolBox_5.setFont(font7)
        self.tool_box_state_5 = QWidget()
        self.tool_box_state_5.setObjectName(u"tool_box_state_5")
        self.tool_box_state_5.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_13 = QScrollArea(self.tool_box_state_5)
        self.scrollArea_13.setObjectName(u"scrollArea_13")
        self.scrollArea_13.setGeometry(QRect(20, 0, 561, 171))
        self.scrollArea_13.setWidgetResizable(True)
        self.scrollAreaWidgetContents_13 = QWidget()
        self.scrollAreaWidgetContents_13.setObjectName(u"scrollAreaWidgetContents_13")
        self.scrollAreaWidgetContents_13.setGeometry(QRect(0, 0, 559, 169))
        self.grb_StateName_12 = QGroupBox(self.scrollAreaWidgetContents_13)
        self.grb_StateName_12.setObjectName(u"grb_StateName_12")
        self.grb_StateName_12.setGeometry(QRect(10, 10, 541, 131))
        self.grb_StateName_12.setFont(font7)
        self.listWidget_RE_DFATab_StateName = QListWidget(self.grb_StateName_12)
        self.listWidget_RE_DFATab_StateName.setObjectName(u"listWidget_RE_DFATab_StateName")
        self.listWidget_RE_DFATab_StateName.setGeometry(QRect(20, 20, 501, 101))
        self.scrollArea_13.setWidget(self.scrollAreaWidgetContents_13)
        self.toolBox_5.addItem(self.tool_box_state_5, u"State")
        self.page_Alphabet_5 = QWidget()
        self.page_Alphabet_5.setObjectName(u"page_Alphabet_5")
        self.page_Alphabet_5.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_14 = QScrollArea(self.page_Alphabet_5)
        self.scrollArea_14.setObjectName(u"scrollArea_14")
        self.scrollArea_14.setGeometry(QRect(20, 10, 561, 141))
        self.scrollArea_14.setWidgetResizable(True)
        self.scrollAreaWidgetContents_14 = QWidget()
        self.scrollAreaWidgetContents_14.setObjectName(u"scrollAreaWidgetContents_14")
        self.scrollAreaWidgetContents_14.setGeometry(QRect(0, 0, 559, 139))
        self.grb_StateName_13 = QGroupBox(self.scrollAreaWidgetContents_14)
        self.grb_StateName_13.setObjectName(u"grb_StateName_13")
        self.grb_StateName_13.setGeometry(QRect(10, 10, 541, 121))
        self.listWidget_RE_DFATab_Alphabet = QListWidget(self.grb_StateName_13)
        self.listWidget_RE_DFATab_Alphabet.setObjectName(u"listWidget_RE_DFATab_Alphabet")
        self.listWidget_RE_DFATab_Alphabet.setGeometry(QRect(10, 10, 521, 101))
        self.scrollArea_14.setWidget(self.scrollAreaWidgetContents_14)
        self.toolBox_5.addItem(self.page_Alphabet_5, u"Alphabet")
        self.page_Transaction_5 = QWidget()
        self.page_Transaction_5.setObjectName(u"page_Transaction_5")
        self.page_Transaction_5.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_15 = QScrollArea(self.page_Transaction_5)
        self.scrollArea_15.setObjectName(u"scrollArea_15")
        self.scrollArea_15.setGeometry(QRect(20, 0, 561, 161))
        self.scrollArea_15.setWidgetResizable(True)
        self.scrollAreaWidgetContents_15 = QWidget()
        self.scrollAreaWidgetContents_15.setObjectName(u"scrollAreaWidgetContents_15")
        self.scrollAreaWidgetContents_15.setGeometry(QRect(0, 0, 559, 159))
        self.tableWidget_RE_DFATab_Transaction = QTableWidget(self.scrollAreaWidgetContents_15)
        if (self.tableWidget_RE_DFATab_Transaction.columnCount() < 3):
            self.tableWidget_RE_DFATab_Transaction.setColumnCount(3)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_RE_DFATab_Transaction.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_RE_DFATab_Transaction.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_RE_DFATab_Transaction.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        self.tableWidget_RE_DFATab_Transaction.setObjectName(u"tableWidget_RE_DFATab_Transaction")
        self.tableWidget_RE_DFATab_Transaction.setGeometry(QRect(0, 0, 581, 181))
        self.scrollArea_15.setWidget(self.scrollAreaWidgetContents_15)
        self.toolBox_5.addItem(self.page_Transaction_5, u"Transaction")
        self.label_22 = QLabel(self.page_3)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(250, 250, 81, 51))
        self.label_22.setFont(font1)
        self.lbl_result_DFA_inital_state = QLabel(self.page_3)
        self.lbl_result_DFA_inital_state.setObjectName(u"lbl_result_DFA_inital_state")
        self.lbl_result_DFA_inital_state.setGeometry(QRect(410, 250, 261, 51))
        self.lbl_result_DFA_inital_state.setFont(font1)
        self.lbl_result_DFA_final_state = QLabel(self.page_3)
        self.lbl_result_DFA_final_state.setObjectName(u"lbl_result_DFA_final_state")
        self.lbl_result_DFA_final_state.setGeometry(QRect(410, 270, 261, 51))
        self.lbl_result_DFA_final_state.setFont(font1)
        self.label_23 = QLabel(self.page_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(250, 270, 91, 51))
        self.label_23.setFont(font1)
        self.toolBox_2.addItem(self.page_3, u"DFA")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.toolBox_6 = QToolBox(self.page_5)
        self.toolBox_6.setObjectName(u"toolBox_6")
        self.toolBox_6.setGeometry(QRect(60, 0, 611, 261))
        self.toolBox_6.setFont(font7)
        self.tool_box_state_6 = QWidget()
        self.tool_box_state_6.setObjectName(u"tool_box_state_6")
        self.tool_box_state_6.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_16 = QScrollArea(self.tool_box_state_6)
        self.scrollArea_16.setObjectName(u"scrollArea_16")
        self.scrollArea_16.setGeometry(QRect(20, 0, 561, 171))
        self.scrollArea_16.setWidgetResizable(True)
        self.scrollAreaWidgetContents_16 = QWidget()
        self.scrollAreaWidgetContents_16.setObjectName(u"scrollAreaWidgetContents_16")
        self.scrollAreaWidgetContents_16.setGeometry(QRect(0, 0, 559, 169))
        self.grb_StateName_14 = QGroupBox(self.scrollAreaWidgetContents_16)
        self.grb_StateName_14.setObjectName(u"grb_StateName_14")
        self.grb_StateName_14.setGeometry(QRect(10, 10, 541, 131))
        self.grb_StateName_14.setFont(font7)
        self.listWidget_RE_NFATab_StateName = QListWidget(self.grb_StateName_14)
        self.listWidget_RE_NFATab_StateName.setObjectName(u"listWidget_RE_NFATab_StateName")
        self.listWidget_RE_NFATab_StateName.setGeometry(QRect(20, 20, 501, 101))
        self.scrollArea_16.setWidget(self.scrollAreaWidgetContents_16)
        self.toolBox_6.addItem(self.tool_box_state_6, u"State")
        self.page_Alphabet_6 = QWidget()
        self.page_Alphabet_6.setObjectName(u"page_Alphabet_6")
        self.page_Alphabet_6.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_17 = QScrollArea(self.page_Alphabet_6)
        self.scrollArea_17.setObjectName(u"scrollArea_17")
        self.scrollArea_17.setGeometry(QRect(20, 10, 561, 141))
        self.scrollArea_17.setWidgetResizable(True)
        self.scrollAreaWidgetContents_17 = QWidget()
        self.scrollAreaWidgetContents_17.setObjectName(u"scrollAreaWidgetContents_17")
        self.scrollAreaWidgetContents_17.setGeometry(QRect(0, 0, 559, 139))
        self.grb_StateName_15 = QGroupBox(self.scrollAreaWidgetContents_17)
        self.grb_StateName_15.setObjectName(u"grb_StateName_15")
        self.grb_StateName_15.setGeometry(QRect(10, 10, 541, 121))
        self.listWidget_RE_NFATab_Alphabet = QListWidget(self.grb_StateName_15)
        self.listWidget_RE_NFATab_Alphabet.setObjectName(u"listWidget_RE_NFATab_Alphabet")
        self.listWidget_RE_NFATab_Alphabet.setGeometry(QRect(10, 10, 521, 101))
        self.scrollArea_17.setWidget(self.scrollAreaWidgetContents_17)
        self.toolBox_6.addItem(self.page_Alphabet_6, u"Alphabet")
        self.page_Transaction_6 = QWidget()
        self.page_Transaction_6.setObjectName(u"page_Transaction_6")
        self.page_Transaction_6.setGeometry(QRect(0, 0, 611, 180))
        self.scrollArea_18 = QScrollArea(self.page_Transaction_6)
        self.scrollArea_18.setObjectName(u"scrollArea_18")
        self.scrollArea_18.setGeometry(QRect(20, 0, 561, 161))
        self.scrollArea_18.setWidgetResizable(True)
        self.scrollAreaWidgetContents_18 = QWidget()
        self.scrollAreaWidgetContents_18.setObjectName(u"scrollAreaWidgetContents_18")
        self.scrollAreaWidgetContents_18.setGeometry(QRect(0, 0, 559, 159))
        self.tableWidget_RE_NFATab_Transaction = QTableWidget(self.scrollAreaWidgetContents_18)
        if (self.tableWidget_RE_NFATab_Transaction.columnCount() < 3):
            self.tableWidget_RE_NFATab_Transaction.setColumnCount(3)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_RE_NFATab_Transaction.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_RE_NFATab_Transaction.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_RE_NFATab_Transaction.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        self.tableWidget_RE_NFATab_Transaction.setObjectName(u"tableWidget_RE_NFATab_Transaction")
        self.tableWidget_RE_NFATab_Transaction.setGeometry(QRect(0, 0, 581, 181))
        self.scrollArea_18.setWidget(self.scrollAreaWidgetContents_18)
        self.toolBox_6.addItem(self.page_Transaction_6, u"Transaction")
        
        self.lbl_result_NFA_final_state = QLabel(self.page_5)
        self.lbl_result_NFA_final_state.setObjectName(u"lbl_result_NFA_final_state")
        self.lbl_result_NFA_final_state.setGeometry(QRect(410, 270, 261, 51))
        self.lbl_result_NFA_final_state.setFont(font1)
        self.label_24 = QLabel(self.page_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(250, 250, 81, 51))
        self.label_24.setFont(font1)
        self.lbl_result_NFA_inital_state = QLabel(self.page_5)
        self.lbl_result_NFA_inital_state.setObjectName(u"lbl_result_NFA_inital_state")
        self.lbl_result_NFA_inital_state.setGeometry(QRect(410, 250, 261, 51))
        self.lbl_result_NFA_inital_state.setFont(font1)
        self.label_25 = QLabel(self.page_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(250, 270, 91, 51))
        self.label_25.setFont(font1)
        
        self.toolBox_2.addItem(self.page_5, u"NFA")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.lbl_result_Are_languages_equvalent = QLabel(self.page_6)
        self.lbl_result_Are_languages_equvalent.setObjectName(u"lbl_result_Are_languages_equvalent")
        self.lbl_result_Are_languages_equvalent.setGeometry(QRect(450, 140, 271, 51))
        self.lbl_result_Are_languages_equvalent.setFont(font6)
        self.lbl_result_Are_languages_equvalent.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_Are_languages_equvalent.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_15 = QLabel(self.page_6)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(160, 10, 191, 51))
        self.label_15.setFont(font1)
        self.btn_Save_Expression_2 = QPushButton(self.page_6)
        self.btn_Save_Expression_2.setObjectName(u"btn_Save_Expression_2")
        self.btn_Save_Expression_2.setGeometry(QRect(320, 80, 111, 31))

        self.btn_Save_Expression_2.clicked.connect(self.on_btn_Save_Expression_2)

        self.txt_Expression_2 = QTextEdit(self.page_6)
        self.txt_Expression_2.setObjectName(u"txt_Expression_2")
        self.txt_Expression_2.setEnabled(True)
        self.txt_Expression_2.setGeometry(QRect(260, 20, 231, 31))
        self.txt_Expression_2.setFont(font4)
        self.txt_Expression_2.setMouseTracking(False)
        self.txt_Expression_2.setAutoFillBackground(False)
        self.txt_Expression_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_Expression_2.setUndoRedoEnabled(True)
        self.lbl_result_is_there_a_relation = QLabel(self.page_6)
        self.lbl_result_is_there_a_relation.setObjectName(u"lbl_result_is_there_a_relation")
        self.lbl_result_is_there_a_relation.setGeometry(QRect(450, 210, 271, 51))
        self.lbl_result_is_there_a_relation.setFont(font6)
        self.lbl_result_is_there_a_relation.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_is_there_a_relation.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_16 = QLabel(self.page_6)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(200, 140, 191, 51))
        self.label_16.setFont(font1)
        self.label_19 = QLabel(self.page_6)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(200, 210, 191, 51))
        self.label_19.setFont(font1)
        self.toolBox_2.addItem(self.page_6, u"Compare languages")
        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(280, 210, 191, 51))
        self.label_26.setFont(font1)
        self.label_26.setAlignment(Qt.AlignCenter)
        self.lbl_result_degree = QLabel(self.groupBox_3)
        self.lbl_result_degree.setObjectName(u"lbl_result_degree")
        self.lbl_result_degree.setGeometry(QRect(570, 210, 121, 51))
        self.lbl_result_degree.setFont(font6)
        self.lbl_result_degree.setLayoutDirection(Qt.LeftToRight)
        self.lbl_result_degree.setAlignment(Qt.AlignCenter)

        self.tabWidget.addTab(self.regular_language_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.txt_DFAName.setCurrentIndex(0)
        self.toolBox_3.setCurrentIndex(0)
        self.toolBox_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.grb_StateName.setTitle(QCoreApplication.translate("MainWindow", u"State Name:", None))
        self.btn_add_StateName.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.cb_finall_state.setText(QCoreApplication.translate("MainWindow", u"finall state", None))
        self.btn_remove_StateName.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.tool_box_state), QCoreApplication.translate("MainWindow", u"State", None))
        self.grb_StateName_2.setTitle(QCoreApplication.translate("MainWindow", u"Alphabet:", None))
        self.btn_add_Alphabet.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btn_remove_Alphabet.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_Alphabet), QCoreApplication.translate("MainWindow", u"Alphabet", None))
        self.grb_StateName_3.setTitle(QCoreApplication.translate("MainWindow", u"Transaction", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"current state:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"transaction:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"target state:", None))
        self.btn_add_Transaction.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        ___qtablewidgetitem = self.tableWidget_Transaction.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Transaction", None));
        ___qtablewidgetitem1 = self.tableWidget_Transaction.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Current state", None));
        ___qtablewidgetitem2 = self.tableWidget_Transaction.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Target state", None));
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_Transaction), QCoreApplication.translate("MainWindow", u"Transaction", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Initial state: ", None))
        self.groupBox_2.setTitle("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Is empty language?", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Is finite?", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Enter your string", None))
#if QT_CONFIG(tooltip)
        self.textEdit_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.lbl_result_test_string.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.txt_DFAName.setItemText(self.txt_DFAName.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Test string", None))
        self.grb_StateName_7.setTitle(QCoreApplication.translate("MainWindow", u"State Name:", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.tool_box_state_3), QCoreApplication.translate("MainWindow", u"State", None))
        self.grb_StateName_8.setTitle("")
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_Alphabet_3), QCoreApplication.translate("MainWindow", u"Alphabet", None))
        ___qtablewidgetitem3 = self.tableWidget_Minimize_Transaction.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Transaction", None));
        ___qtablewidgetitem4 = self.tableWidget_Minimize_Transaction.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Current state", None));
        ___qtablewidgetitem5 = self.tableWidget_Minimize_Transaction.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Target state", None));
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_Transaction_3), QCoreApplication.translate("MainWindow", u"Transaction", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Initial state:", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Final states:", None))
        self.lbl_result_inital_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.lbl_result_final_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        
        
        
        
        self.txt_DFAName.setItemText(self.txt_DFAName.indexOf(self.Minimize), QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.grb_StateName_9.setTitle(QCoreApplication.translate("MainWindow", u"State Name:", None))
        self.btn_EquivalentTab_State_Add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.cb_EquivalentTab_finall_state.setText(QCoreApplication.translate("MainWindow", u"finall state", None))
        self.btn_EquivalentTab_State_Remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.tool_box_state_4), QCoreApplication.translate("MainWindow", u"State", None))
        self.grb_StateName_10.setTitle(QCoreApplication.translate("MainWindow", u"Alphabet:", None))
        self.btn_EquivalentTab_Alphabet_Add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btn_EquivalentTab_Alphabet_Remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_Alphabet_4), QCoreApplication.translate("MainWindow", u"Alphabet", None))
        ___qtablewidgetitem6 = self.tableWidget_EquivalentTab_Transaction.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Transaction", None));
        ___qtablewidgetitem7 = self.tableWidget_EquivalentTab_Transaction.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Current state", None));
        ___qtablewidgetitem8 = self.tableWidget_EquivalentTab_Transaction.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Target state", None));
        self.btn_add_Transaction_3.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.grb_StateName_11.setTitle("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"current state:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"transaction:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"target state:", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_Transaction_4), QCoreApplication.translate("MainWindow", u"Transaction", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Initial state: ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"DFA name: ", None))
#if QT_CONFIG(tooltip)
        self.txt_Equivalent_DFAName.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_Equivalent.setText(QCoreApplication.translate("MainWindow", u"Equivalent", None))
        self.lbl_result_is_Equivalent.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.txt_DFAName.setItemText(self.txt_DFAName.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Equivalent", None))
        self.lbl_result_is_empty_language.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.lbl_result_is_finite.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"All strings:", None))
        self.lbl_result_allStrings.setText(QCoreApplication.translate("MainWindow", u"Result", None))
#if QT_CONFIG(tooltip)
        self.txt_DFAName_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"DFA name: ", None))
        self.btn_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DFA_tab), QCoreApplication.translate("MainWindow", u"DFA", None))
        self.groupBox_3.setTitle("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Expression:", None))
#if QT_CONFIG(tooltip)
        self.txt_Expression_1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_Save_Expression_1.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Regular language?", None))
        self.lbl_result_is_regular_language.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.grb_StateName_12.setTitle(QCoreApplication.translate("MainWindow", u"State Name:", None))
        self.toolBox_5.setItemText(self.toolBox_5.indexOf(self.tool_box_state_5), QCoreApplication.translate("MainWindow", u"State", None))
        self.grb_StateName_13.setTitle("")
        self.toolBox_5.setItemText(self.toolBox_5.indexOf(self.page_Alphabet_5), QCoreApplication.translate("MainWindow", u"Alphabet", None))
        ___qtablewidgetitem9 = self.tableWidget_RE_DFATab_Transaction.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Transaction", None));
        ___qtablewidgetitem10 = self.tableWidget_RE_DFATab_Transaction.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Current state", None));
        ___qtablewidgetitem11 = self.tableWidget_RE_DFATab_Transaction.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Target state", None));
        self.toolBox_5.setItemText(self.toolBox_5.indexOf(self.page_Transaction_5), QCoreApplication.translate("MainWindow", u"Transaction", None))
        
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Initial state:", None))
        self.lbl_result_DFA_inital_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.lbl_result_DFA_final_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Final states:", None))
        
        
        
        
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"DFA", None))
        self.grb_StateName_14.setTitle(QCoreApplication.translate("MainWindow", u"State Name:", None))
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.tool_box_state_6), QCoreApplication.translate("MainWindow", u"State", None))
        self.grb_StateName_15.setTitle("")
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_Alphabet_6), QCoreApplication.translate("MainWindow", u"Alphabet", None))
        ___qtablewidgetitem12 = self.tableWidget_RE_NFATab_Transaction.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Transaction", None));
        ___qtablewidgetitem13 = self.tableWidget_RE_NFATab_Transaction.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Current state", None));
        ___qtablewidgetitem14 = self.tableWidget_RE_NFATab_Transaction.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Target state", None));
        self.toolBox_6.setItemText(self.toolBox_6.indexOf(self.page_Transaction_6), QCoreApplication.translate("MainWindow", u"Transaction", None))
        
        self.lbl_result_NFA_final_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Initial state:", None))
        self.lbl_result_NFA_inital_state.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Final states:", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"NFA", None))
        self.lbl_result_Are_languages_equvalent.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Expression 2:", None))
        self.btn_Save_Expression_2.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.txt_Expression_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lbl_result_is_there_a_relation.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Are languages \u200b\u200bequivalent?", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Is there a relation?", None))
        
        
        
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"NFA", None))
        self.lbl_result_Are_languages_equvalent.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Expression 2:", None))
        self.btn_Save_Expression_2.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.txt_Expression_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lbl_result_is_there_a_relation.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Are languages \u200b\u200bequivalent?", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Is there a relation?", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_6), QCoreApplication.translate("MainWindow", u"Compare languages", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Degree: ", None))
        self.lbl_result_degree.setText(QCoreApplication.translate("MainWindow", u"Result", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.regular_language_tab), QCoreApplication.translate("MainWindow", u"Regular Language", None))
    # retranslateUi


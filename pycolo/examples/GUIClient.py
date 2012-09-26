#!/usr/bin/env python
""" generated source for module GUIClient """
# package: ch.ethz.inf.vs.californium.examples
import java.awt.BorderLayout

import java.awt.Dimension

import java.awt.GridLayout

import java.awt.event.ActionEvent

import java.awt.event.ActionListener

import java.util.ArrayList

import java.util.List

import java.util.Scanner

import java.util.StringTokenizer

import java.util.regex.Pattern

import javax.swing.BoxLayout

import javax.swing.DefaultComboBoxModel

import javax.swing.JButton

import javax.swing.JComboBox

import javax.swing.JFrame

import javax.swing.JPanel

import javax.swing.JScrollPane

import javax.swing.JSplitPane

import javax.swing.JTextArea

import javax.swing.JTree

import javax.swing.SwingUtilities

import javax.swing.UIManager

import javax.swing.border.EmptyBorder

import javax.swing.border.TitledBorder

import javax.swing.event.TreeSelectionEvent

import javax.swing.event.TreeSelectionListener

import javax.swing.tree.DefaultMutableTreeNode

import javax.swing.tree.DefaultTreeModel

import javax.swing.tree.TreePath

import ch.ethz.inf.vs.californium.coap

# 
#  * A CoAP Client to communicate with other CoAP resources.
#  * 
#  * @author Martin Lanter
#  
class GUIClient(JPanel):
    """ generated source for class GUIClient """
    serialVersionUID = -8656652459991661071L
    DEFAULT_URI = "coap://localhost:5683"
    TESTSERVER_URI = "coap://vs0.inf.ethz.ch:5683"
    COAP_PROTOCOL = "coap://"
    cboTarget = JComboBox()
    txaPayload = JTextArea()
    txaResponse = JTextArea()
    pnlResponse = JPanel()
    responseBorder = TitledBorder()
    dmtRes = DefaultMutableTreeNode()
    dtmRes = DefaultTreeModel()
    treRes = JTree()

    def __init__(self):
        """ generated source for method __init__ """
        super(GUIClient, self).__init__()
        btnGet = JButton("GET")
        btnPos = JButton("POST")
        btnPut = JButton("PUT")
        btnDel = JButton("DELETE")
        btnDisc = JButton("Discovery")
        btnGet.addActionListener(ActionListener())
        btnPos.addActionListener(ActionListener())
        btnPut.addActionListener(ActionListener())
        btnDel.addActionListener(ActionListener())
        btnDisc.addActionListener(ActionListener())
        self.cboTarget = JComboBox()
        self.cboTarget.setEditable(True)
        self.cboTarget.setMinimumSize(self.cboTarget.getPreferredSize())
        self.cboTarget.addItem(self.DEFAULT_URI)
        self.cboTarget.addItem(self.TESTSERVER_URI)
        self.cboTarget.setSelectedIndex(0)
        self.txaPayload = JTextArea("", 8, 50)
        self.txaResponse = JTextArea("", 8, 50)
        self.txaResponse.setEditable(False)
        pnlDisc = JPanel(BorderLayout())
        pnlDisc.add(self.cboTarget, BorderLayout.CENTER)
        pnlDisc.add(btnDisc, BorderLayout.EAST)
        pnlTarget = JPanel(BorderLayout())
        pnlTarget.setBorder(TitledBorder("Target"))
        pnlTarget.add(pnlDisc, BorderLayout.NORTH)
        pnlTarget.setMaximumSize(Dimension(Integer.MAX_VALUE, pnlTarget.getPreferredSize().height))
        pnlButtons = JPanel(GridLayout(1, 4, 10, 10))
        pnlButtons.setBorder(EmptyBorder(10, 10, 10, 10))
        pnlButtons.add(btnGet)
        pnlButtons.add(btnPos)
        pnlButtons.add(btnPut)
        pnlButtons.add(btnDel)
        pnlRequest = JPanel(BorderLayout())
        pnlRequest.setBorder(TitledBorder("Request"))
        pnlRequest.add(JScrollPane(self.txaPayload), BorderLayout.CENTER)
        pnlRequest.add(pnlButtons, BorderLayout.SOUTH)
        self.pnlResponse = JPanel(BorderLayout())
        self.responseBorder = TitledBorder("Response")
        self.pnlResponse.setBorder(self.responseBorder)
        self.pnlResponse.add(JScrollPane(self.txaResponse))
        panelC = JPanel()
        panelC.setLayout(BoxLayout(panelC, BoxLayout.Y_AXIS))
        panelC.add(pnlTarget)
        panelC.add(pnlRequest)
        splReqRes = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        splReqRes.setContinuousLayout(True)
        splReqRes.setResizeWeight(0.5)
        splReqRes.setTopComponent(panelC)
        splReqRes.setBottomComponent(self.pnlResponse)
        self.dmtRes = DefaultMutableTreeNode("Resources")
        self.dtmRes = DefaultTreeModel(self.dmtRes)
        self.treRes = JTree(self.dtmRes)
        scrRes = JScrollPane(self.treRes)
        scrRes.setPreferredSize(Dimension(200, scrRes.getPreferredSize().height))
        panelE = JPanel(BorderLayout())
        panelE.setBorder(TitledBorder("Resources"))
        panelE.add(scrRes, BorderLayout.CENTER)
        setLayout(BorderLayout())
        splCE = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
        splCE.setContinuousLayout(True)
        splCE.setResizeWeight(0.5)
        splCE.setLeftComponent(panelE)
        splCE.setRightComponent(splReqRes)
        add(splCE)
        self.treRes.addTreeSelectionListener(TreeSelectionListener())
        discover()

    def discover(self):
        """ generated source for method discover """
        self.dmtRes.removeAllChildren()
        self.dtmRes.reload()
        request = GETRequest()
        request.setURI(self.COAP_PROTOCOL + getHost() + "/.well-known/core")
        request.registerResponseHandler(ResponseHandler())
        execute(request)

    def populateTree(self, ress):
        """ generated source for method populateTree """
        root = Node("Resource")
        for res in ress:
            while len(parts):
                if n == None:
                    cur.children.add(n = Node(parts[i]))
                cur = n
                i += 1
        self.dmtRes.removeAllChildren()
        addNodes(self.dmtRes, root)
        self.dtmRes.reload()
        i = 0
        while i < self.treRes.getRowCount():
            self.treRes.expandRow(i)
            i += 1

    def addNodes(self, parent, node):
        """ generated source for method addNodes """
        for n in node.children:
            parent.add(dmt)
            self.addNodes(dmt, n)

    class Node(object):
        """ generated source for class Node """
        name = str()
        children = ArrayList()

        def __init__(self, name):
            """ generated source for method __init__ """
            self.name = name

        def get(self, name):
            """ generated source for method get """
            for c in children:
                if name == c.name:
                    return c
            return None

    class MyPostRequest(POSTRequest):
        """ generated source for class MyPostRequest """

    def performRequest(self, request):
        """ generated source for method performRequest """
        self.txaResponse.setText("no response yet")
        self.responseBorder.setTitle("Response: none")
        self.pnlResponse.repaint()
        request.registerResponseHandler(ResponsePrinter())
        request.setPayload(self.txaPayload.getText())
        request.setURI(self.cboTarget.getSelectedItem().__str__().replace(" ", "%20"))
        execute(request)

    def execute(self, request):
        """ generated source for method execute """
        try:
            request.execute()
        except Exception as ex:
            ex.printStackTrace()

    class ResponsePrinter(ResponseHandler):
        """ generated source for class ResponsePrinter """
        def handleResponse(self, response):
            """ generated source for method handleResponse """
            self.txaResponse.setText(response.getPayloadString())
            self.responseBorder.setTitle("Response: " + CodeRegistry.toString(response.getCode()))
            self.pnlResponse.repaint()

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        setLookAndFeel()
        SwingUtilities.invokeLater(Runnable())

    @classmethod
    def setLookAndFeel(cls):
        """ generated source for method setLookAndFeel """
        try:
            UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName())
        except Exception as e:
            e.printStackTrace()

    def getHost(self):
        """ generated source for method getHost """
        uri = str(self.cboTarget.getSelectedItem())
        st = StringTokenizer(uri, "/")
        st.nextToken()
        host = st.nextToken()
        return host


if __name__ == '__main__':
    import sys
    GUIClient.main(sys.argv)


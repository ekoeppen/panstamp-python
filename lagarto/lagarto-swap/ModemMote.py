from swap.protocol.SwapMote import SwapMote
from swap.protocol.SwapPacket import SwapStatusPacket, SwapCommandPacket, SwapQueryPacket
from swap.protocol.SwapDefs import SwapRegId, SwapState
from swap.protocol.SwapValue import SwapValue
from swap.SwapException import SwapException
from swap.xmltools.XmlDevice import XmlDevice

import time

def trace(fn):
    "Returns a traced version of the input function."
    from itertools import chain
    def wrapped(*v, **k):
        name = fn.__name__
        print "%s(%s)" % (
            name, ", ".join(map(repr, chain(v, k.values()))))
        return fn(*v, **k)
    return wrapped

class ModemMote(SwapMote):
    """
    SWAP mote class
    """
    def cmdRegister(self, regId, value):
        """
        Send command to register and return expected response
        
        @param regId: Register ID
        @param value: New value
        
        @return Expected SWAP status packet sent from mote after reception of this command
        """
        # Update register
	if regId:
        	reg = self.getRegister(regId)
		if reg:
			reg.setValue(value)
        # Don't wait for ack
        return None;


    def qryRegister(self, regId):
        """
        Return register value via status packet
        
        @param regId: Register ID
        """
	self.staRegister(regId)


    def staRegister(self, regId):
        """
        Send SWAP status packet about the current value of the register passed as argument
        
        @param regId: Register ID
        @param value: New value
        """
        # Get register
        reg = self.getRegister(regId)
        # Status packet to be sent
        infPacket = SwapStatusPacket(self.address, regId, reg.value)
        # Send SWAP status packet to server
        infPacket.send(self.server)


    def cmdRegisterWack(self, regId, value):
        """
        Send SWAP command to remote register and wait for confirmation
        
        @param regId: Register ID
        @param value: New value
        
        @return True if ACK is received from mote. Return False otherwise
        """
	self.getRegister(regId).setValue(value)
        return True


    def getRegister(self, regId):
        """
        Get register given its ID
        
        @param regId: Register ID
        
        @return SwapRegister object
        """
	if regId:
	    reg = super(ModemMote, self).getRegister(regId)
	    if reg:
		if regId == 129:
		    l = time.localtime(time.time())
		    reg.setValue(SwapValue("%c%c%c%c%c%c%c" % (l.tm_year % 256, l.tm_year / 256, l.tm_mon, l.tm_mday, l.tm_hour, l.tm_min, l.tm_sec), 7))
	return reg


    def restart(self):
	"""
	Ask mote to restart

	@return True if this command is confirmed from the mote. Return False otherwise
	"""
	return True


    def leaveSync(self):
	"""
	Ask mote to leave SYNC mode (RXON state)

	@return True if this command is confirmed from the mote. Return False otherwise
	"""
	return True


    def __init__(self, server=None, product_code=None, address=0xFF, security=0, nonce=0):
	"""
	Class constructor

	@param server: SWAP server object
	@param product_code: Product Code
	@param address: Mote address
	"""
	super(ModemMote, self).__init__(server, product_code, address, security, nonce)
	self.config_registers = []

<?xml version="1.0" encoding="UTF-8"?>
<!--+ typecastTools.xsl
	|
	| version	1.0.0
	| author	fjacobsen
	| license	copyright kgu-consulting gmbh, 2017
	|
	| provides tools for String typecasts (e.g. return String as bool).
	|
	+-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:kit="publishing-toolkit"
	exclude-result-prefixes="xs kit"
	version="2.0">
	
	<!--+ typecastString
		|
		| "magic" function to determine possible typecasts for arg.
		|
		| arg => input string 
		|
		+-->
	<xsl:function name="kit:typecastString"
		as="item()*">
		<xsl:param name="arg"
			as="xs:string"/>
		
		<xsl:variable name="string"
			select="normalize-space(lower-case($arg))"
			as="xs:string"/>
		
		<xsl:choose>
			<!-- return integer -->
			<xsl:when test="$string castable as xs:integer">
				<xsl:value-of select="xs:integer($string)"/>
			</xsl:when>
			<!-- return double -->
			<xsl:when test="$string castable as xs:double">
				<xsl:value-of select="xs:double($string)"/>
			</xsl:when>
			<!-- return bool -->
			<xsl:when test="$string castable as xs:boolean">
				<xsl:value-of select="xs:boolean($string)"/>
			</xsl:when>
			<!-- return (unformatted) String -->
			<xsl:otherwise>
				<xsl:message>error: <xsl:value-of select="$arg"/> can not be cast to integer, double or bool. unformatted string will be processed.</xsl:message>
				<xsl:value-of select="$arg"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:function>
	
	<xsl:function name="kit:isInteger"
		as="xs:boolean">
		<xsl:param name="arg"
			as="item()"/>
		
		<xsl:value-of select="if($arg castable as xs:integer) then true()
			else false()"/>
	</xsl:function>
	
	<xsl:function name="kit:isDouble"
		as="xs:boolean">
		<xsl:param name="arg"
			as="item()"/>
		
		<xsl:value-of select="if($arg castable as xs:double) then true()
			else false()"/>
	</xsl:function>
	
	<xsl:function name="kit:isBoolean"
		as="xs:boolean">
		<xsl:param name="arg"
			as="item()"/>
		
		<xsl:value-of select="if($arg castable as xs:boolean) then true()
			else false()"/>
	</xsl:function>
</xsl:stylesheet>
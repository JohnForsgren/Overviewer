<?xml version="1.0" encoding="UTF-8"?>
<!--+ cals-table.xsl
	|
	| version	1.0.0
	| author	jweichert
	|
	| LICENSE
	| ================================================================
	| Copyright KGU-Consulting GmbH. All rights reserved.
	| Use is subject to license terms.
	| All intellectual property rights held by KGU-Consulting GmbH Flensburg, Germany.
	| Source codes at KGU's free disposal.
	| 
	| DESCRIPTION
	| ================================================================
	| implements OASIS CALS table standard.
	| 
	+-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:kit="publishing-toolkit"
	exclude-result-prefixes="xs kit"
	version="2.0">
	
	<!--+ set table entry text alignment
		|
		| mapps input alignment to match coding conventions and sass classes.
		|
		+-->
	<xsl:function name="kit:setTableEntryTextAlignmentExt"
		as="xs:string">
		<xsl:param name="textAlignment"
			as="xs:string"/>
		
		<xsl:variable name="align"
			select="normalize-space($textAlignment)"
			as="xs:string"/>
		
		<xsl:choose>
			<xsl:when test="$align = 'left'">
				<xsl:text>ta-left</xsl:text>
			</xsl:when>
			<xsl:when test="$align = 'center'">
				<xsl:text>ta-center</xsl:text>
			</xsl:when>
			<xsl:when test="$align = 'right'">
				<xsl:text>ta-right</xsl:text>
			</xsl:when>
            <xsl:when test="$align = 'justify'">
				<xsl:text>ta-justify</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:function>

<xsl:template match="*[@*[name() = $sourceTag] = 'entry']"
		as="item()*"
		priority="7">
		
		<!-- get column no. -->
		<xsl:variable name="columnNo"
			select="count(preceding-sibling::*) + 1"
			as="xs:integer"/>
		
		<!-- set row span -->
		<xsl:variable name="rowspan"
			select="if(not(empty(@morerows)) and not(@morerows = '')) then xs:integer(@morerows) + 1
				else 1"
			as="xs:integer"/>
		
		<!-- set column span -->
		<xsl:variable name="colspan"
			as="xs:integer">
			<xsl:variable name="start"
				select="if(not(empty(@namest)) and not(@namest = ''))
					then number(translate(@namest, translate(@namest, '0123456789', ''), ''))
					else 1"/>
			<xsl:variable name="end"
				select="if(not(empty(@nameend)) and not(@nameend = ''))
				then number(translate(@nameend, translate(@nameend, '0123456789', ''), ''))
				else 1"/>
			<xsl:value-of select="$end - $start + 1"/>
		</xsl:variable>
		
		<!-- horizontal alignment -->
		<xsl:variable name="align"
			as="xs:string">
			<xsl:choose>
				<!-- entry alignment -->
				<xsl:when test="not(empty(@align)) and not(@align = '')">
					<xsl:value-of select="kit:setTableEntryTextAlignmentExt(@align)"/>
				</xsl:when>
				<!-- row alignment -->
				<xsl:when test="parent::*[not(empty(@align)) and not(@align = '')]">
					<xsl:value-of select="kit:setTableEntryTextAlignmentExt(parent::*/@align)"/>
				</xsl:when>
				<!-- column alignment -->
				<xsl:when test="ancestor::*/*[@colnum = $columnNo][not(empty(@align)) and not(@align = '')]">
					<xsl:value-of select="kit:setTableEntryTextAlignmentExt(ancestor::*/*[@colnum = $columnNo]/@align)"/>
				</xsl:when>
				<!-- table group alignment -->
				<xsl:when test="ancestor::*[@*[name() = $sourceTag] = 'tgroup'][not(empty(@align)) and not(@align = '')]">
					<xsl:value-of select="kit:setTableEntryTextAlignmentExt(ancestor::*[@*[name() = $sourceTag] = 'tgroup']/@align)"/>
				</xsl:when>
				<!-- default: empty (alignment will be handled by browser defaults and css) -->
				<xsl:otherwise>
					<xsl:text/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		
		<!-- vertical alignment -->
		<xsl:variable name="valign"
			as="xs:string">
			<xsl:choose>
				<!-- entry -->
				<xsl:when test="not(empty(@valign)) and not(@valign = '')">
					<xsl:value-of select="kit:setTableEntryVerticalAlignment(@valign)"/>
				</xsl:when>
				<!-- row alignment -->
				<xsl:when test="parent::*[not(empty(@valign)) and not(@valign = '')]">
					<xsl:value-of select="kit:setTableEntryVerticalAlignment(parent::*/@valign)"/>
				</xsl:when>
				<!-- column alignment -->
				<xsl:when test="ancestor::*/*[@colnum = $columnNo][not(empty(@valign)) and not(@valign = '')]">
					<xsl:value-of select="kit:setTableEntryTextAlignmentExt(ancestor::*/*[@colnum = $columnNo]/@valign)"/>
				</xsl:when>
				<!-- table group alignment -->
				<xsl:when test="ancestor::*[@*[name() = $sourceTag] = 'tgroup'][not(empty(@valign)) and not(@valign = '')]">
					<xsl:value-of select="kit:setTableEntryVerticalAlignment(ancestor::*[@*[name() = $sourceTag] = 'tgroup']/@valign)"/>
				</xsl:when>
				<!-- default: empty (alignment will be handled by browser defaults and css) -->
				<xsl:otherwise>
					<xsl:text/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		
		<xsl:variable name="colsep"
				select="if(not(empty(@colsep)) and not(@colsep = ''))
				then @colsep
				else '1'"/>
		<xsl:variable name="rowsep"
				select="if(not(empty(@rowsep)) and not(@rowsep = ''))
				then @rowsep
				else '1'"/>
		<xsl:variable name="outputclass"
				select="if(not(empty(@outputclass)) and not(@outputclass = ''))
				then @outputclass
				else ''"/>
		<xsl:variable name="rotate"
				select="if(not(empty(@rotate)) and not(@rotate = ''))
				then @rotate
				else ''"/>

		<xsl:element name="{if(ancestor::*[@*[name() = $sourceTag] = 'thead']) then 'th'
			else 'td'}">
			<xsl:attribute name="class"
				select="kit:buildClass(($align, $valign, $outputclass))"/>
			<xsl:attribute name="rowspan"
				select="$rowspan"/>
			<xsl:attribute name="colspan"
				select="$colspan"/>
			<xsl:attribute name="colsep"
				select="$colsep"/>
			<xsl:attribute name="rowsep"
				select="$rowsep"/>
			<xsl:attribute name="rotate"
				select="$rotate"/>
				<!-- add meta data (with prefix) -->
						<xsl:call-template name="addAttribute">
							<xsl:with-param name="include"
								select="(@*)"
								as="node()*"/>
							<xsl:with-param name="prefix"
								select="'data'"
								as="xs:string"/>
            			</xsl:call-template>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="*[@*[name() = $sourceTag] = 'row']"
		as="item()*"
		priority="3">
		
		<tr>
		<!-- add meta data (with prefix) -->
						<xsl:call-template name="addAttribute">
							<xsl:with-param name="include"
								select="(@*)"
								as="node()*"/>
							<xsl:with-param name="prefix"
								select="'data'"
								as="xs:string"/>
            			</xsl:call-template>
			<xsl:apply-templates/>
		</tr>
	</xsl:template>

	<xsl:template match="*[@*[name() = $sourceTag] = 'table']"
		as="item()*"
		priority="3">
		
		<!-- table style (class). used for stylings like "zebra". -->
		<xsl:variable name="tableStyle"
			select="if(not(empty(@outputclass)) and not(@outputclass = '')) then @outputclass
				else ''"
			as="xs:string"/>
		
		<!-- add table intro element -->
		<xsl:apply-templates select="*[@*[name() = $sourceTag] = 'tableintro']"/>
		
		<table id="{@id}"
			class="{kit:buildClass(($tableStyle))} TEST">
			
			<xsl:call-template name="addAttribute">
				<xsl:with-param name="include"
					select="(@*)"
					as="node()*"/>
				<xsl:with-param name="prefix"
					select="'data'"
					as="xs:string"/>
			</xsl:call-template>
			
			<xsl:apply-templates select="* except *[@*[name() = $sourceTag] = 'tableintro']"/>
		</table>
	</xsl:template>

			

    </xsl:stylesheet>
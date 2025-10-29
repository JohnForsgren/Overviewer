<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:kit="publishing-toolkit" exclude-result-prefixes="xs kit" version="2.0">
    <xsl:output method="xhtml" indent="no"/>
    <xsl:strip-space elements="*"/>

    <!-- define a global variable to hold all fn elements -->
    <xsl:variable name="footnotes" select="//fn" />

    <xsl:template match="table">
        <xsl:copy>
            <xsl:apply-templates select="@*[not(name()='class')]"/>

            <xsl:attribute name="class">
                <xsl:value-of select="@class"/>
                <xsl:if test="contains(@data-outputclass, 'option-dl-standard')">
                    <xsl:text> keep-together</xsl:text>
                </xsl:if>
            </xsl:attribute>

            <xsl:choose>
                <xsl:when test="contains(@class, 'option-dl-standard')">
                    <colgroup>
                        <col width="65pt"/>
                        <col/>
                    </colgroup>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>

            <xsl:apply-templates select="node()" mode="copy"/>

            <xsl:for-each select=".//fn[contains(@data-outputclass, 'table-fn')]">
                <xsl:apply-templates select="." mode="table-fn">
                    <xsl:with-param name="footnote-num" select="index-of($footnotes, .)"/>
                </xsl:apply-templates>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
    

    <xsl:template match="td[.//fn[contains(@data-outputclass, 'table-fn')]]">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
            <xsl:attribute name="class">
                <xsl:value-of select=".//fn[contains(@data-outputclass, 'table-fn')]/@data-outputclass" />
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="fn" mode="table-fn">
        <xsl:param name="footnote-num"/>
        <tr>
            <td>
                <xsl:copy-of select="@data-outputclass"/>
                <xsl:attribute name="colspan">
                    <xsl:value-of select="count(ancestor::table[1]//tr[1]/td)"/>
                </xsl:attribute>
                <sup>
                    <xsl:value-of select="$footnote-num"/>
                </sup>
                <xsl:value-of select="."/>
            </td>
        </tr>
    </xsl:template>

    <!-- template that matches any element with a data-outputclass attribute, excluding table elements -->
    <xsl:template match="*[@data-outputclass or @data-align][not(self::table)]">
        <!-- create a copy of the current element -->
        <xsl:copy>
            <xsl:copy-of select="@*[not(name()='class' or name()='data-outputclass' or name()='data-align')]" />
            <xsl:attribute name="class">
                <xsl:choose>
                    <xsl:when test="contains(@data-outputclass, 'option-dl-standard')">
                        <xsl:value-of select="concat(@class, ' keep-together')" />
                    </xsl:when>
                    <xsl:when test="contains(@data-outputclass, '-') and not(contains(@class, @data-outputclass))">
                        <xsl:value-of select="concat(@class, ' ', @data-outputclass, if(@data-align != '') then concat(' ta-', @data-align) else '', if(@data-valign != '') then concat(' va-', @data-valign) else '', if(local-name() = 'fig' or local-name() = 'figure') then ' keep-together' else '')" />
                    </xsl:when>
                    <xsl:when test="@class and not(contains(@class, translate(@data-outputclass, '_', '-')))">
                        <xsl:value-of select="concat(@class, ' ', translate(@data-outputclass, '_', '-'), if(@data-align != '') then concat(' ta-', @data-align) else '', if(@data-valign != '') then concat(' va-', @data-valign) else '', if(local-name() = 'fig' or local-name() = 'figure') then ' keep-together' else '')" />
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="concat(translate(@data-outputclass, '_', '-'), if(@data-align != '') then concat(' ta-', @data-align) else '', if(@data-valign != '') then concat(' va-', @data-valign) else '', if(local-name() = 'fig' or local-name() = 'figure') then ' keep-together' else '')" />
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="@*|node()" mode="copy">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" mode="copy"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="entry" mode="copy">
        <xsl:copy>
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="fn" mode="copy">
        <xsl:copy>
            <xsl:copy-of select="@*"/>
            <!-- output footnote number only when data-outputclass isn't 'table-fn' -->
            <xsl:if test="@data-outputclass != 'table-fn'">
                <sup>
                    <xsl:value-of select="index-of($footnotes, .)"/>
                </sup>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="@data-outputclass = 'table-fn'">
                    <xsl:text> See table </xsl:text>
                    <xsl:value-of select="ancestor::table/caption/@data-tableCount"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
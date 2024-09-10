import React from 'react';
import DropDown from '../components/DropDown';
import { Col, Row, Input, Button } from 'antd';
import './styles/Grid.css';

const GridView = () => {
  return (
    <>
      <Row align="middle" className="input-button-row">
        <Col span={18}>
          <Input placeholder="Type Message" />
        </Col>
        <Col span={6}>
          <Button type="primary" style={{ width: '100%' }}>
            Send
          </Button>
        </Col>
      </Row>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Row>
            <Col span={24}><DropDown /></Col>
          </Row>
          <Row>
            <Col span={24}><pre className="grid-pre">Preformatted text here</pre></Col>
          </Row>
        </Col>
        <Col span={12}>
          <Row>
            <Col span={24}><DropDown /></Col>
          </Row>
          <Row>
            <Col span={24}><pre className="grid-pre">Preformatted text here</pre></Col>
          </Row>
        </Col>
      </Row>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Row>
            <Col span={24}><DropDown /></Col>
          </Row>
          <Row>
            <Col span={24}><pre className="grid-pre">Preformatted text here</pre></Col>
          </Row>
        </Col>
        <Col span={12}>
          <Row>
            <Col span={24}><DropDown /></Col>
          </Row>
          <Row>
            <Col span={24}><pre className="grid-pre">Preformatted text here</pre></Col>
          </Row>
        </Col>
      </Row>
    </>
  );
};

export default GridView;
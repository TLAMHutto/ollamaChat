import React from 'react';
import { Col, Row } from 'antd';
import { Input, Button } from 'antd';
import './styles/Grid.css';

const GridView = () => {
  return (
    <>
      <Row align="middle" className="input-button-row">
        <Col span={18}>
          <Input placeholder="Basic usage" />
        </Col>
        <Col span={6}>
          <Button type="primary" style={{ width: '100%' }}>
            Send
          </Button>
        </Col>
      </Row>
      <Row>
        <Col className='grid-row' span={12}>col-12</Col>
        <Col className='grid-row' span={12}>col-12</Col>
      </Row>
      <Row>
        <Col className='grid-row' span={12}>col-12</Col>
        <Col className='grid-row' span={12}>col-12</Col>
      </Row>
    </>
  );
};

export default GridView;
